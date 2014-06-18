###############################################
# Algorithm for getting movie recommendations #
###############################################

from recommendations.models import Movie, Preferences_2


def recommendation_algorithm(movies_user_watched, movie, theuser):
    # get users that watched same movie as our user
    queryset_by_movie = Preferences_2.objects.filter(
        movie=movie).filter(rating__gt=3).exclude(user=theuser).values()

    movies_user_watched_names = \
        [mov.get('movie_id') for mov in movies_user_watched]

    list_of_users = []
    list_of_similarities = []

    # for each of users that watched the same movie as our user
    # find wich other movies they rated and with rate > 3
    for pref_record_2 in queryset_by_movie:
        user = pref_record_2.get('user')
        queryset_by_user = Preferences_2.objects.filter(
            user=user).filter(rating__gt=3).values()

        count_occurences = 0  # number of movies that both users watched
        similarity_index_by_all_user_movies = 0

        # for each of that movies check if it's the movie that also
        # our user rated
        for movie_1 in queryset_by_user:
            try:
                current_movie = [
                    mov for mov in movies_user_watched
                    if mov.get('movie_id') == movie_1.get('movie_id')
                ][0]
            except:
                current_movie = {}

            if movie_1.get('movie_id') in movies_user_watched_names:
                # calculate similarity between
                # ratings of both users for that movie.
                # check if rating exists, if not set it to 3
                # (3 is average prediction).
                if not movie_1.get('rating'):
                    if movie_1.get('rating') is None:
                        movie_1_rating = 3
                    else:
                        movie_1_rating = movie_1.get('rating')
                    if current_movie.get('rating') is None:
                        current_movie_rating = 3
                    else:
                        current_movie_rating = current_movie.get('rating')
                    similarity_index_by_movie = abs(
                        movie_1_rating -
                        current_movie_rating
                    )
                    count_occurences += 1
                    similarity_index_by_all_user_movies += (
                        similarity_index_by_movie)
                else:
                    if movie_1.get('rating') is None:
                        movie_1_rating = 3
                    else:
                        movie_1_rating = movie_1.get('rating')
                    if current_movie.get('rating') is None:
                        current_movie_rating = 3
                    else:
                        current_movie_rating = current_movie.get('rating')
                    similarity_index_by_movie = abs(
                        movie_1_rating -
                        current_movie_rating
                    )
                    count_occurences += 1
                    similarity_index_by_all_user_movies += (
                        similarity_index_by_movie)

        # calculate similarity between two users.
        # we are dividing similarity_index_by_all_user_movies with
        # count_occurences to get average similarity.
        # The smaller the result (closer to 0), similarity is better.
        # Also check if they both viewed at least 3 same movies.
        if count_occurences >= 3:
            similarity_index_by_user = float(
                similarity_index_by_all_user_movies) / count_occurences
            list_of_users.append(user)
            list_of_similarities.append(similarity_index_by_user)

    recommendation_list = get_recommendations(
        list_of_users, list_of_similarities, movies_user_watched_names)

    return recommendation_list


def get_recommendations(
        list_of_users, list_of_similarities, movies_user_watched_names):
    """
    Function for getting list of recommendations.
    We recommend movies that most similar user/s rated with 5.
    If there isn't 10 such movies then we fill recommendations list
    with most popular movies.
    """
    recommendations_list = []
    recommendations_counter = 0

    # check if similar users exist
    if len(list_of_users) >= 1:
        for u in list_of_users:
            # check if recommendation_list is full.
            # If not, fill it with more movies. If yes, break.
            if recommendations_counter < 10:
                # minimal value of similarity is the best
                index = list_of_similarities.index(min(list_of_similarities))
                # first get the most similar user,
                # in other iterations get next most similar....
                similar_user = list_of_users[index]

                # set hight number at the place of best similarity to
                # avoid choosing it the next time
                list_of_similarities[index] = 1000

                queryset_by_similar_user = Preferences_2.objects.filter(
                    user=similar_user).filter(rating=5).values()
                list_queryset_by_similar_user = \
                    [mov.get('movie_id') for mov in queryset_by_similar_user]

                # For each movie that most similar user rated with 5
                # check if recommendations_list is full,
                # if movie is already in the list
                # and if it's also movie that our user watched already.
                for movie in list_queryset_by_similar_user:
                    if recommendations_counter < 10:
                        if movie not in recommendations_list:
                            if movie not in movies_user_watched_names:
                                recommendations_list.append(movie)
                                recommendations_counter += 1
                    else:
                        break
                else:
                    break
            else:
                break

        # if recommendations_list is still not full get the most popular movies
        if recommendations_counter < 20:
            most_viewed = Movie.objects.all().order_by('-view_counter')[0:50]
            most_popular = sorted(
                most_viewed, key=lambda o: o.rating, reverse=True)

            for movie in most_popular:
                if recommendations_counter < 10:
                    print movie.id
                    if movie.id not in recommendations_list:
                        if movie.id not in movies_user_watched_names:
                            recommendations_list.append(movie.id)
                            recommendations_counter += 1

    # If there is no similarity for our user show him most popular movies.
    else:
        # We take 50 most viewed movies, then select 10 best rated of those 50.
        most_viewed = Movie.objects.all().order_by('-view_counter')[0:50]
        most_popular = sorted(
            most_viewed, key=lambda o: o.rating, reverse=True)
        for movie in most_popular:
            if recommendations_counter < 10:
                if movie.id not in movies_user_watched_names:
                    recommendations_list.append(movie.id)
                    recommendations_counter += 1

    return recommendations_list


def get_most_popular(movies_user_watched):
    """
    Function for getting most popular movies.
    """
    recommendations_counter = 0
    recommendations_list = []
    movies_user_watched_names = \
        [mov.get('movie_id') for mov in movies_user_watched]

    most_viewed = Movie.objects.all().order_by('-view_counter')[0:50]
    most_popular = sorted(most_viewed, key=lambda o: o.rating, reverse=True)

    for movie in most_popular:
        if recommendations_counter < 10:
            if movie.id not in movies_user_watched_names:
                recommendations_list.append(movie.id)
                recommendations_counter += 1

    return recommendations_list
