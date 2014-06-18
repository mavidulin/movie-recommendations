import logging
logger = logging.getLogger(__name__)

from django.db.models import Max
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from .models import Movie, Preferences_2, MovieRecom
from .recommendation_algorithm import (
    recommendation_algorithm,
    get_most_popular)


class IndexView(ListView):
    """
    View for showing homepage with list of all movies.
    """
    model = Movie
    queryset = model.objects.all().order_by('name')
    template_name = 'index.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # check if user has user_cid in cookie.
        try:
            user_cid = self.request.session['user_cid']
            recommended_movies = MovieRecom.objects.filter(user=user_cid)
            context['recommendations'] = recommended_movies
        except:
            # make him user_cid (user first time on site)
            max_user_cid = Preferences_2.objects.all().aggregate(
                Max('user'))['user__max']
            user_cid = max_user_cid + 1
            self.request.session['user_cid'] = user_cid

        return context


class SearchView(ListView):
    """
    View for showing the page with search results.
    """
    model = Movie
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        searchString = self.kwargs['search']
        movie_list = self.model.objects.filter(name__icontains=searchString)

        # ======= Pagination for custom queryset ===========
        page_size = 15
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                movie_list, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'movie_list': queryset
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'movie_list': movie_list
            }
        # ======= END Pagination for custom queryset ===========

        context.update(kwargs)
        context['search_check'] = True
        # get movies that were recommended to the user
        user_cid = self.request.session['user_cid']
        recommended_movies = MovieRecom.objects.filter(user=user_cid)
        context['recommendations'] = recommended_movies

        return context


class DetailView(DetailView):
    """
    View for showing page with details about movie,
    and running the algorithm for getting recommendations.
    """
    model = Movie
    pk_url_kwarg = 'pk'
    template_name = 'detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        movie = int(self.kwargs['pk'])
        theuser = self.request.session['user_cid']
        movies_user_watched = Preferences_2.objects.filter(
            user=theuser).values()

        # Check if user already opened that movie.
        # Check if user already rated movie.
        # If he did, then save rating to context.
        movie_in_movies_user_watched = False
        for m_2 in movies_user_watched:
            if m_2['movie_id'] == movie:
                movie_in_movies_user_watched = True
                if m_2['rating'] is not None:
                    existing_rating = m_2['rating']
                    context['existing_rating'] = existing_rating

                break

        # If user opened that movie for the first time save
        # the record in Preferences_2
        if movie_in_movies_user_watched is False:
            movieObj = Movie.objects.get(id=movie)
            p = Preferences_2(user=theuser, movie=movieObj)
            p.save()
            # append currently opened movie to movies_user_watched
            movies_user_watched = list(movies_user_watched)
            movies_user_watched.insert(0, {'movie_id': movie})

        # When user opens movie for first and second time
        # just recommend most popular movies.
        if len(movies_user_watched) < 2:
            if not movies_user_watched:
                movies_user_watched = []

            recommendations = get_most_popular(movies_user_watched)
        else:
            recommendations = recommendation_algorithm(
                movies_user_watched, movie, theuser)

        # From MovieRecom delete existing recommendations for the user
        # and save new ones.
        MovieRecom.objects.filter(user=theuser).delete()

        # from movie ids in recommendations get Movie objects
        recommendations_list = []
        for recom_movie in recommendations:
            m = Movie.objects.get(id=recom_movie)
            # Save recommmended movies to MovieRecom
            # to be able to show them on homepage.
            mr = MovieRecom(user=theuser, movie=m)
            mr.save()
            recommendations_list.append(m)

        context['recommendations'] = recommendations_list

        return context


def RatingView(request, **kwargs):
    rating = int(kwargs.get('rating'))
    movie = int(kwargs.get('movie'))
    user = request.session['user_cid']

    record = Preferences_2.objects.filter(user=user).filter(movie=movie)[0]
    existing_rating = record.rating

    if existing_rating is None:
        # save rating to preferences table
        record.rating = rating
        record.save()
        # save sum_rating, view_counter, and average rating to movie table
        m = Movie.objects.get(id=movie)
        view_counter = m.view_counter + 1
        m.view_counter = view_counter

        rating_sum = m.rating_sum + rating
        m.rating_sum = rating_sum

        avg_rating = rating_sum / view_counter
        m.rating = avg_rating
        m.save()
    else:
        # save new rating to preferences table
        record.rating = rating
        record.save()
        # save NEW sum_rating, and average rating to movie table
        m = Movie.objects.get(id=movie)

        # add new rating and delete old one
        rating_sum = m.rating_sum - existing_rating + rating
        m.rating_sum = rating_sum

        avg_rating = rating_sum / m.view_counter
        m.rating = avg_rating
        m.save()

    return HttpResponse('Ok')
