from django.conf.urls import patterns, url

from .views import IndexView, SearchView, DetailView, RatingView


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view()),
    url(r'^search/(?P<search>[\w ]+)/$', SearchView.as_view()),
    url(r'^detail/(?P<pk>\d+)/$', DetailView.as_view()),
    url(r'^rating/(?P<rating>\d+)/(?P<movie>\d+)/$', RatingView),
)
