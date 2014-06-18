import os
from django.core.management.base import BaseCommand
from recommendations.models import Movie, Preferences


class Command(BaseCommand):

    def handle(self, *args, **options):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'prefs.csv')

        data = open(filename, 'r')
        data = data.readlines()

        for line in data:
            listFromLine = line.split(',')

            user = listFromLine[0].decode('iso-8859-1').encode('utf8')
            movie_cid = listFromLine[1].decode('iso-8859-1').encode('utf8')
            rating = listFromLine[2].decode('iso-8859-1').encode('utf8')

            movie_obj = Movie.objects.filter(cid=movie_cid)[0]

            string = '{} - {} - {}'.format(user, movie_cid, rating)
            self.stdout.write(string)

            p = Preferences(user=user, movie=movie_obj, rating=rating)
            p.save()
