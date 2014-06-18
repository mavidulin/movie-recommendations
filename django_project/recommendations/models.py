import logging
logger = logging.getLogger(__name__)

from django.db import models


class Movie(models.Model):
    # custom id
    cid = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    # average rating for movie
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True)
    view_counter = models.IntegerField(default=0)
    # sum of all ratings
    rating_sum = models.IntegerField(default=0)

    def __unicode__(self):
        return u'{0} ({1}) - {2}'.format(
            self.name, self.rating, self.view_counter)


class Preferences_2(models.Model):
    user = models.IntegerField()
    movie = models.ForeignKey(Movie)
    # rating of user for movie
    rating = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return u'{0} - {1} ({2})'.format(
            self.user, self.movie.name, self.rating)


# db table that stores movie recommendations for user
# (will be used to show recommendations when user returns to homepage)
class MovieRecom(models.Model):
    user = models.IntegerField()
    movie = models.ForeignKey(Movie)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.user, self.movie.name)


############## Models for algorithm_tester.py #######################

class Preferences(models.Model):
    user = models.IntegerField()
    movie = models.ForeignKey(Movie)
    # rating of user for movie
    rating = models.IntegerField()

    def __unicode__(self):
        return u'{0} - {1} ({2})'.format(
            self.user, self.movie.name, self.rating)


class UserRelations(models.Model):
    user_1 = models.IntegerField(null=True, blank=True)
    user_2 = models.IntegerField(null=True, blank=True)
    similarity_coeff = models.DecimalField(
        max_digits=6, decimal_places=5, null=True, blank=True)

    def __unicode__(self):
        return u'user {0} - user {1} - similarity {2}'.format(
            self.user_1, self.user_2, self.similarity_coeff)


class TestProcessedUsers(models.Model):
    user_cid = models.IntegerField()

############## End Models for algorithm_tester.py #######################
