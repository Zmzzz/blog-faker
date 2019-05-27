from django.shortcuts import render,HttpResponse,redirect
from bbs.form import regform
from bbs import models
from django.http import JsonResponse
from django.contrib import auth
import json
from django.db.models import F
from django.db.models import Count
# Create your views here.
# 博客主页
def index(request):
    # 查询出所有文章
    all_article=models.Article.objects.all()
    return render(request,'index.html',{'all_article':all_article})
# 用户退出登录（使用auth模块）
def login_out(request):
    auth.logout(request)
    return redirect('/login/')
# 登录页面
def login(request):
    if request.method=='POST':
        ret = {'status': 0, 'msg': ''}
        # 先进行判断验证码是否正确
        # 获取存在session中的验证码
        valid_code=request.POST.get('valid_code')
        if valid_code.upper()==request.session.get('valid_code').upper():
            ret['msg']='/index/'
            # auth模块验证账号或者密码是否正确
            username = request.POST.get('username')
            pwd = request.POST.get('pwd')
            user = auth.authenticate(username=username, password=pwd)
            if user:
                auth.login(request, user)
            else:
                ret['status']=1
                ret['msg']='账号或密码错误'
        else:
            ret['status']=1
            ret['msg'] = '验证码错误'
        return JsonResponse(ret)
    return render(request, 'login.html')
# 验证码
def get_valid_img(request):
# 第二种方法
#     print(111)
#     import PIL
#     import random
#     def random_valid_img_color():
#         return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
#     from PIL import Image
#     image=Image.new('RGB',(250,40),random_valid_img_color())
#     f=open('valid_code.png','wb')
#     image.save(f,'png')
#     with open('valid_code.png','rb') as f:
#         data=f.read()
#     return HttpResponse(data)
# 第三种方法
#     import PIL
#     import random
#     def random_valid_img_color():
#         return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
#     from PIL import Image
#     image=Image.new('RGB',(250,40),random_valid_img_color())
#     from io import BytesIO
# # 直接存入内存中，更加快速
#     f=BytesIO()
#     image.save(f,'png')
#     data=f.getvalue()
#     f.close()
#     return HttpResponse(data)
# 第四种方法，加入数字()()
    import PIL
    import random
    # 随机颜色
    def random_valid_img_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    from PIL import Image,ImageDraw,ImageFont
    image=Image.new('RGB',(250,40),random_valid_img_color())
    draw=ImageDraw.Draw(image)
    font=ImageFont.truetype('static/font/kumo.ttf',28)
    valid_code=''
    for i in range(5):
         random_int=str(random.randint(0,9))
         random_upper_Eng=chr(random.randint(65,90))
         random_low_Eng=chr(random.randint(97,122))
         choice=random.choice([random_int,random_low_Eng,random_upper_Eng])
         valid_code=valid_code+choice
         draw.text([i*48,0],choice,random_valid_img_color(),font=font)
    print('系统随机生成的输入的验证码', valid_code)
    request.session['valid_code']=valid_code
    width=240
    high=80
    for i in range(10):
        x1=random.randint(0,width)
        y1=random.randint(0,high)
        x2 = random.randint(0, width)
        y2 = random.randint(0, high)
        draw.line([x1,y1,x2,y2],fill=random_valid_img_color())
    from io import BytesIO
    f=BytesIO()
    image.save(f,'png')
    data=f.getvalue()
    f.close()
    return HttpResponse(data)
# 用户注册（使用form表单）
def register(request):
    form_obj=regform()
    if request.method=='POST':
        # 将前端的数据填进入到form_obj
        form_obj=regform(request.POST)
        # 验证form表单是否有错误
        if form_obj.is_valid():
            # 获取头像文件
            avatar=request.FILES.get('avatar_file')
            print('request.file',request.FILES)
            print('avatar的值',avatar)
            # 删除多余的确认密码
            form_obj.cleaned_data.pop('re_pwd')
            if avatar==None:
                models.UserInfo.objects.create_user(**form_obj.cleaned_data)
                return redirect('/login/')
            # 创建新用户
            models.UserInfo.objects.create_user(**form_obj.cleaned_data,avatar=avatar)
            return redirect('/login/')
    return render(request,'register.html',{'form_obj':form_obj})
# 用户注册（使用ajax）
def register_ajax(request):
    form_obj=regform()
    if request.method=='POST':
        ret={'status':0,'msg':''}
        # 将前端的数据填进入到form_obj
        form_obj=regform(request.POST)
        # 验证form表单是否有错误
        if form_obj.is_valid():
            # 获取头像文件
            avatar=request.FILES.get('avatar')
            print('ajax版request.file', request.FILES)
            print(request.POST)
            print('ajax版avatar的值', avatar)
            # 删除多余的确认密码
            form_obj.cleaned_data.pop('re_pwd')
            ret['msg']='/login/'
            # 创建新用户
            models.UserInfo.objects.create_user(**form_obj.cleaned_data,avatar=avatar)
            return JsonResponse(ret)
        else:
            ret['status']=1
            ret['msg']=form_obj.errors
            return JsonResponse(ret)
    return render(request, 'register-ajax.html', {'form_obj': form_obj})
# 个人主页
        # 1.获取到路由传来的用户名username
def home(request,username):
    # 通过名字找到user对象
    user_obj=models.UserInfo.objects.filter(username=username).first()
    # 找到该作者
    if user_obj:
        # 1.找到作者的所有文章
        article_list=models.Article.objects.filter(user_id=user_obj.nid)
        # 2.找到作者的博客
   #      blog=user_obj.blog
   #      # 3.找到该作者博客下面的所有分类,然后找到每个分类下面的文章数
   #      category_list= models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values('title','c')
   #      # 找到该作者博客下面的所有标签, 然后找到每个标签下面的文章数
   #      tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values('title', 'c')
   #      # 找到该作者博客下面的所有日期，然后找到每个日期下面的文章数
   #      time_list=models.Article.objects.filter(user=user_obj).extra(select={"time": "date(create_time)"} ).values('time').annotate(c=Count('nid')).values('time', 'c')
   # # 未找到直接报错
    else:
        return HttpResponse('404')
    return render(request,'home.html',{
        'user_obj':user_obj,
        'article_list':article_list,
    })

# 文章详情
def article_Detail(request,username,pk):
    print('username,pk',username,pk)
    # 通过名字找到user对象
    user_obj = models.UserInfo.objects.filter(username=username).first()
    # 找到该作者
    if user_obj:
        # 1.找到文章
        article = models.Article.objects.filter(nid=pk).first()
        #
        # print(article)
        # # 2.找到作者的博客
        # blog = user_obj.blog
        # # 3.找到该作者博客下面的所有分类,然后找到每个分类下面的文章数
        # category_list = models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values('title', 'c')
        # # 找到该作者博客下面的所有标签, 然后找到每个标签下面的文章数
        # tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values('title', 'c')
        # # 找到该作者博客下面的所有日期，然后找到每个日期下面的文章数
        # time_list = models.Article.objects.filter(user=user_obj).extra(select={"time": "date(create_time)"}).values(
        #     'time').annotate(c=Count('nid')).values('time', 'c')
        # 未找到直接报错
        # 找到当前文章的所有评论
        comment_list=models.Comment.objects.filter(article=article)

    else:
        return HttpResponse('404')
    return render(request, 'article_detail.html', {
        'user_obj': user_obj,
        'article': article,
        'comment_list':comment_list,
    })

# 文章点赞/踩
def up_down(request):
    print(request.POST)
    is_up=json.loads(request.POST.get('is_up'))
    article_pk=request.POST.get('article_pk')
    user=request.user
    response={'state':True,'user':True}
    try:
        models.ArticleUpDown.objects.create(user=user,is_up=is_up,article_id=article_pk),
        if is_up:
            models.Article.objects.filter(nid=article_pk).update(up_count=F('up_count')+1)
        else:
            models.Article.objects.filter(nid=article_pk).update(down_count=F('down_count') + 1)
    except:
        ret=models.ArticleUpDown.objects.filter(article_id=article_pk,user=user).first().is_up
        response = {'state': False,'is_up':ret}
    return JsonResponse(response)



# 文章评论
def comment(request):
    print(request.POST)
    article_pk=int(request.POST.get('article_pk'))
    content=request.POST.get('comment_info')
    user=request.user
    pid = request.POST.get('pid')
    if pid=='':
        models.Comment.objects.create(article_id=article_pk,user=user,content=content)
    else:
        pid = int(request.POST.get('pid'))
        models.Comment.objects.create(article_id=article_pk, user=user, content=content,parent_comment_id=pid)
    return HttpResponse("ok")
# 评论数
def comment_tree(request,article_pk):
    comment_list=list(models.Comment.objects.filter(article_id=article_pk).values('pk','content','parent_comment_id'))
    print(comment_list)
    return JsonResponse(comment_list,safe=False)

# 后台管理，添加文章
def add_article(request):
    return render(request,'add_article.html')

def upload(request):
    print(request.FILES)
    return HttpResponse('ok')



# def get_picture(request):
#     f = open('valid_code.png', 'wb')
#     #     image.save(f,'png')
#     #     with open('valid_code.png','rb') as f:
#     #         data=f.read()
#     #     return HttpResponse(data)
