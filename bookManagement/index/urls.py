from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^parent/$',parent_views),
	url(r'^child/$',child_views),
]

urlpatterns +=[
	url(r'^add_author/$',add_author_views),
	url(r'^add_book/$',add_book_views),
	url(r'^add_publisher/$', add_publisher_views),
]


urlpatterns += [
	url(r'^get_author/$', get_author_views),
	url(r'^filter_author/$',filter_author_views),
	url(r'^author_list/$', author_list_views),
	url(r'^del_user/(\d+)/$',del_user_views,name='del'),
]

urlpatterns += [
	url(r'^update_author/$',update_author_views),
	url(r'^doF/$',doF_views),
	url(r'^doQ/$',doQ_views),
	url(r'^raw/$',raw_views),
]    

urlpatterns += [
	url(r'^all_authors/$',all_authors_views),
]

urlpatterns +=[
	url(r'^oto/$',oto_views),
	url(r'^otm/$',otm_views),
	url(r'^mtm/$',mtm_views),
]

urlpatterns +=[
	url(r'^name_count',name_count_views),
	url(r'^title_count',title_count_views),
]	