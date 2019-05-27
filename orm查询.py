import os
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
    import django
    django.setup()
    # 1.查询某个分类对应的文章数，先查出有多少分类，然后按分类分组，查询出文章数
    from bbs import models
    from django.db.models import Count
    user=models.UserInfo.objects.filter(username='zmm').first()
    blog=user.blog
    # ret=models.Article.objects.filter(user_id=user.nid)
    # print(ret)
    # ret1=models.Category.objects.filter(blog=blog)
    # print(ret1)
    # ret=models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values('title','c')
    # print(ret)
    # 标签分类
    # ret=models.Tag.objects.filter(blog=blog)
    # print(ret)
    # ret = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values('title','c')
    # print(ret)
    # 日期分类
    ret=models.Article.objects.filter(user=user).extra(
        select={"time": "date(create_time)"}
    ).values('time').annotate(c=Count('nid')).values('time','c')
    print(ret)
