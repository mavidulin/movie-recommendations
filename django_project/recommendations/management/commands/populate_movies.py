import os
from django.core.management.base import BaseCommand
from recommendations.models import Movie


class Command(BaseCommand):

    def handle(self, *args, **options):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'movies.csv')

        data = open(filename, 'r')
        data = data.readlines()

        forbidden_chars = ['|', '~', '{', '}']

        for line in data:
            listFromLine = line.split(',', 1)

            cid = listFromLine[0].decode('iso-8859-1').encode('utf8')
            name_list = listFromLine[1].decode(
                'iso-8859-1').encode('utf8').split('\n')
            name = name_list[0]

            forbidden_chars_found = False
            for char in forbidden_chars:
                if char in name:
                    forbidden_chars_found = True
                    break

            if forbidden_chars_found is not True:
                print cid

            string = '{}, {}'.format(cid, name)
            self.stdout.write(string)

            m = Movie(cid=cid, name=name, rating=1)
            m.save()
