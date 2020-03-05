from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User


# Create your views here.


# 登录页面
def login(request):
    return render(request, "login.html")


# # 登录操作
# def login_action(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#
#         if username == '' or password == '':
#             messages = "用户名和密码不能为空"
#             return render(request, 'login.html', {'message': messages})
#
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)  # 登录
#             request.session['user'] = username  # 将session 信息记录到浏览器
#             response = HttpResponseRedirect('/event_manage/')
#             return response
#         else:
#             messages = "用户名或密码错误"
#             return render(request, 'login.html', {'message': messages})


# 登录操作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = "用户名和密码不能为空！"
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    auth.login(request, user)  # 登录账号admin，密码panpan123
                    request.session['user'] = username  # 将session 信息记录到浏览器
                    response = HttpResponseRedirect('/event_manage/')
                    return response
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'login.html', {"message": message})


def forget_password(request):
    return render(request, "PeppaPig.html")


# 发布会列表页
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '')  # 读取浏览器session
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})


# 嘉宾列表页
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('user', '')
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})

# 嘉宾名称搜索
@login_required
def search_guest(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("guest_name", "")
    guest_list = Guest.objects.filter(guest_name=search_name)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": guest_list})


# 签到页面
@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', {'event': event})


# 签到动作
@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.'})

    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.'})

    result = Guest.objects.get(phone=phone, event_id=event_id)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': "user has sign in."})
    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in success!',
                                                   'guest': result})


# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/login/')
    return response