from django.conf.urls import url
from bbs import views
urlpatterns = [
    url(r'^',views.add_article),
    url(r'^comment_tree/(?P<article_pk>\d+)/',views.comment_tree),
    url(r'^comment/',views.comment),
    url(r'^up_down/',views.up_down),
    url(r'(?P<username>\w+)/article/(?P<pk>\d+)',views.article_Detail),
    # 如果不加?P<username>是位置参数，home（request，args），如果加了是命名参数，home（request,username）
    url(r'(?P<username>\w+)',views.home),
]