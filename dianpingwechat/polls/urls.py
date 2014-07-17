from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from polls.models import Poll

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Poll.objects.order_by('-pub_date')[:5],
            context_object_name='latest_poll_list',
            template_name='polls/index.html'),
        name='index'),
    url(r'^(?P<poll_id>\d+)/$','polls.views.roomDetail', name='detail'),
    url(r'^(?P<poll_id>\d+)/result/$', 'polls.views.result', name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote', name='vote'),
    url(r'^menu/(?P<shop_id>\d+)/(?P<poll_id>\d+)$', 'polls.views.menu', name='menu'),
    url(r'^menu2/(?P<shop_id>\d+)/(?P<poll_id>\d+)$', 'polls.views.menu2', name='menu2'),
    url(r'^adddish/(?P<poll_id>\d+)/(?P<dish_name>.*)$', 'polls.views.adddish', name='adddish'),
    url(r'^deldish/(?P<poll_id>\d+)/(?P<dish_name>.*)$', 'polls.views.deldish', name='deldish'),
    url(r'^checkorder/(?P<poll_id>\d+)$', 'polls.views.checkorder', name='checkorder'),
)