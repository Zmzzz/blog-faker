"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from bbs.views import register,index,login,register_ajax,get_valid_img,login_out,upload
from bbs import urls as  blog_url
from  bbs import  views
# 导入media
from django.views.static import serve
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^reg/',register),
    url(r'^index/',index),
    url(r'^login/',login),
    url(r'^login_out/',login_out),
    url(r'^reg_ajax/',register_ajax),
    url(r'^get_valid_img/',get_valid_img),
    # 二级路由，将所有blog开头的路由，都交给app下面的urls处理
    url(r'^blog/',include( blog_url)),
    # media相关的路由设置
    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    url(r'^upload/uplaod/',upload),
]
