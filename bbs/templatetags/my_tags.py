from django import template
from bbs import models
from django.db.models import Count
register=template.Library()

@register.inclusion_tag("left_menu.html")
def get_left_menu(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog
    # 3.找到该作者博客下面的所有分类,然后找到每个分类下面的文章数
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values('title', 'c')
    # 找到该作者博客下面的所有标签, 然后找到每个标签下面的文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values('title', 'c')
    # 找到该作者博客下面的所有日期，然后找到每个日期下面的文章数
    time_list = models.Article.objects.filter(user=user_obj).extra(select={"time": "date(create_time)"}).values(
        'time').annotate(c=Count('nid')).values('time', 'c')
    return {
        'category_list': category_list,
        'tag_list': tag_list,
        'time_list': time_list
    }