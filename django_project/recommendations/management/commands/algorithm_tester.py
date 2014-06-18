import os
from django.core.management.base import BaseCommand
from recommendations.models import Preferences, UserRelations
import math


class Command(BaseCommand):

    def handle(self, *args, **options):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'test_results.txt')
        data = open(filename, 'w')

        # first we take users from preferences table for testing purposes
        def get_users_for_testing():
            preferences_queryset = Preferences.objects.all()
            # keep track of which user is processed
            users_processed = []

            for record in preferences_queryset:
                # define how many users will be processed
                if len(users_processed) < 2:
                    theuser = record.user

                    if theuser not in users_processed:
                        # get all movies/ratings for user we are processing
                        prefs_by_user_queryset = Preferences.objects.filter(
                            user=theuser).values()
                        users_processed.append(theuser)

                        # for each movie/rating our user rated run algorithm
                        for pref_record in prefs_by_user_queryset:
                            movie = pref_record.get('movie')

                            # run recommendation algorithm
                            recommendation_algorithm(
                                prefs_by_user_queryset, movie, theuser)

            # after finishing algoritm (and finding similar users
            # for each "test" user) calculate accuracy.
            get_rms()

        def recommendation_algorithm(movies_user_watched, movie, theuser):
            # get users that watched the same movie as our user
            queryset_by_movie = Preferences.objects.filter(movie=movie).filter(
                rating__gt=3).exclude(user=theuser).values()

            movies_user_watched_names = \
                [mov.get('movie_id') for mov in movies_user_watched]

            list_of_users = []
            list_of_similarities = []

            # for each of users that watched the same movie as our user
            # find wich other movies they rated and with rate > 3
            for pref_record_2 in queryset_by_movie:
                user = pref_record_2.get('user')
                queryset_by_user = Preferences.objects.filter(
                    user=user).filter(rating__gt=3).values()

                count_occurences = 0  # number of movies both users watched
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
                                current_movie_rating = \
                                    current_movie.get('rating')
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
                                current_movie_rating = \
                                    current_movie.get('rating')
                            similarity_index_by_movie = abs(
                                movie_1_rating -
                                current_movie_rating
                            )
                            count_occurences += 1
                            similarity_index_by_all_user_movies += (
                                similarity_index_by_movie)

                # Calculate similarity between two users.
                # we are dividing similarity_index_by_all_user_movies with
                # count_occurences to get average similarity.
                # The smaller the result (closer to 0), similarity is better.
                # Also check if they both viewed at least 3 same movies.
                if count_occurences >= 3:
                    similarity_index_by_user = float(
                        similarity_index_by_all_user_movies) / count_occurences
                    list_of_users.append(user)
                    list_of_similarities.append(similarity_index_by_user)

            # check if there is at least one user with similarity
            if len(list_of_users) >= 1:
                # for testing get only one most similar user!
                best_similarity = min(list_of_similarities)
                index_of_best_similarity = \
                    list_of_similarities.index(best_similarity)
                most_similar_user = list_of_users[index_of_best_similarity]
                our_user = theuser

                if UserRelations.objects.filter(
                        user_2=most_similar_user, user_1=our_user):

                    user_relation_obj = UserRelations.objects.filter(
                        user_2=most_similar_user, user_1=our_user)[0]
                    existing_simil_coeff = user_relation_obj.similarity_coeff
                    new_simil_coeff = \
                        (existing_simil_coeff + best_similarity) / 2
                    user_relation_obj.similarity_coeff = new_simil_coeff
                    user_relation_obj.save()
                else:
                    user_relation_obj = UserRelations(
                        user_1=our_user, user_2=most_similar_user,
                        similarity_coeff=best_similarity)
                    user_relation_obj.save()

        def get_rms():
            """
            Function for getting accuracy of algorithm.

            We guess which rating would every "test" user give to movies
            he already rated and calculate how many times we guessed correct
            rating.

            For each movie of each "test" user we propose rating of his most
            similar user (who rated that movie).
            We also keep track of all differences in ratings between
            "test" users and their most similar users and calculate rms
            ("something like average mistake in guessing grades").
            """
            all_movies_count = 0
            all_bingos = 0
            # list for all rms (of all "test" users and all their movies)
            list_of_rms = []
            # keep track which users were processed
            #because we are going throuh user_relations table
            list_of_processed_users = []

            for relation_record in UserRelations.objects.all():
                user_1 = relation_record.user_1
                # check if we already processed that user
                if user_1 not in list_of_processed_users:
                    list_of_processed_users.append(user_1)
                    prefs_by_user_1_queryset = \
                        Preferences.objects.filter(user=user_1)

                    # counter of how many times we proposed correct rating
                    # (for each user separately)
                    bingo_counter_by_user = 0
                    # get all records of similarity for one "test" user
                    user_relation_queryset = UserRelations.objects.filter(
                        user_1=user_1).order_by('similarity_coeff')

                    list_of_processed_movies = []
                    # list of differences in rating with power of 2 ( v^2 )
                    list_of_difference = []

                    # First we compare our user's ratings with
                    # ratings of his most similar user,
                    # then if some movies are not compared try to find
                    # that movies in movies list of next most similar user.
                    for relation in user_relation_queryset:
                        # check if we still have movies to process
                        if len(list_of_processed_movies) < \
                                len(prefs_by_user_1_queryset):

                            user_2 = relation.user_2
                            # get movies from similar user
                            queryset_by_user_2 = Preferences.objects.filter(
                                user=user_2)

                            # for each movie of our "test" user, if that movie
                            # is not yet processed and if it can be found in
                            # similar user's movies list do rating comaprison.
                            for user_1_movie in prefs_by_user_1_queryset:
                                if user_1_movie.movie not in \
                                        list_of_processed_movies:

                                    if queryset_by_user_2.filter(
                                            movie=user_1_movie.movie):

                                        difference = user_1_movie.rating - \
                                            queryset_by_user_2.filter(
                                                movie=user_1_movie.movie)[0] \
                                            .rating

                                        # If we proposed correct rating than
                                        # increase bingo_counter by one.
                                        if difference == 0:
                                            bingo_counter_by_user += 1
                                        list_of_difference.append(
                                            math.pow(difference, 2))
                                        list_of_processed_movies.append(
                                            user_1_movie.movie)
                        else:
                            # if all "test" user movies are processed and user_
                            # relation for loop is still going just break it
                            break

                    # if there is no match for some movies that our user rated
                    # with movies most similar users rated then for those
                    # movies set difference to max value ( 4 )
                    if len(list_of_processed_movies) < \
                            len(prefs_by_user_1_queryset):

                        num_of_not_processed_movies = len(
                            prefs_by_user_1_queryset) - len(
                            list_of_processed_movies)
                        l = [math.pow(4, 2)] * num_of_not_processed_movies
                        list_of_difference.extend(l)

                    # summ differences for one "test" user
                    sum_of_differences = sum(list_of_difference)
                    if sum_of_differences > 0:
                        # calculate root mean square
                        rms = math.sqrt(
                            sum_of_differences / len(prefs_by_user_1_queryset))
                        list_of_rms.append(rms)
                    else:
                        list_of_rms.append(0)

                    # number of movies for one "test" user
                    movies_count_by_user = len(prefs_by_user_1_queryset)

                    all_movies_count += movies_count_by_user

                    # percentage of bingo_by_user
                    bingo_percentage_by_user = \
                        float(bingo_counter_by_user) / movies_count_by_user \
                        * 100

                    all_bingos += bingo_counter_by_user

                    text = "Korisnik: " + str(user_1) + "\n" + "\n" \
                        "Broj ocjenjenih filmova: " + \
                        str(movies_count_by_user) + "\n" + \
                        "Broj pogodaka ocjena: " + \
                        str(bingo_counter_by_user) + "\n" + \
                        "Postotak pogodaka: " + \
                        str('%.2f' % bingo_percentage_by_user) + "\n" + \
                        "RMS: " + str('%.3f' % rms) + "\n" + "\n" + "\n"

                    data.write(text)

            # calculate average rms from all "test" users ratings
            average_rms = sum(list_of_rms) / len(list_of_rms)
            # calculate percatage of testing set in set of all preferences
            testing_set_percentage = float(all_movies_count) / \
                Preferences.objects.all().count() * 100
            percentage_of_accuracy = float(all_bingos) / all_movies_count * 100

            text_2 = "** Skup za testiranje: " + str(all_movies_count) + \
                " (" + str('%.2f' % testing_set_percentage) + "%) **" + \
                "\n" + "\n" + \
                "Ukupni RMS: " + str('%.3f' % average_rms) + "\n" + \
                "POSTOTAK TOCNOSTI ALGORITMA: " + \
                str('%.2f' % percentage_of_accuracy)

            data.write(text_2)
            data.close()

        # Run!
        get_users_for_testing()
