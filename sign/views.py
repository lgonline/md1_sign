from django.shortcuts import render

# Create your views here.

# import MySQLdb
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def index(request):
    return render(request,'sign/index.html')

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)

            request.session['user'] = username

            response = HttpResponseRedirect('/event_mgmt/')

            return response
        else:
            return render(request,'sign/index.html',{'error':'username or password is error!'})

    pass

@login_required
def event_mgmt(request):
    event_list = Event.objects.all()
    username = request.session.get('user','')
    return render(request,'sign/event_mgmt.html',{'user':username,'events':event_list})


@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,'sign/event_mgmt.html',{'user':username,'events':event_list})

@login_required
def guest_mgmt(request):
    guest_list = Guest.objects.all()

    # 增加分页器,查询出的所有嘉宾列表guest_list防到Paginator中，每页5条数据
    paginator = Paginator(guest_list,5)
    page = request.GET.get('page')

    try:
        # 通过get请求得到当前要显示第几页的数据
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，取第一个页面的数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围，取最后一页
        contacts = paginator.page(paginator.num_pages)

    username = request.session.get('user','')
    return render(request,'sign/guest_mgmt.html',{'user':username,'guests':contacts})

@login_required
def sign_index(request,eid):
    # get_object_or_404默认调用django的
    event = get_object_or_404(Event,id=eid)
    return render(request,'sign/sign_index.html',{'event':event})

@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id=eid)
    phone = request.POST.get('phone','')
    print(phone)

    # 查询手机号在guest表种是否存在
    result = Guest.objects.filter(phone=phone)
    if not result:
        # 如果手机号不再guest表中，提示phone错误
        return render(request,'sign/sign_index.html',{'event':event,'hint':'电话号码不存在.!'})

    # 查询手机号和发布会id是否在guest表中，如果为空，则手机号与发布会不匹配
    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,'sign/sign_index.html',{'event':event,'hint':'发布会活动或者手机号错误.'})


    result = Guest.objects.get(phone=phone, event_id=eid)
    # 判断嘉宾的状态是否为true，如果是true，则表示已经签到过
    if result.sign:
        return render(request,'sign/sign_index.html',{'event':event,'hint':'已经签到.'})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request,'sign/sign_index.html',{'event':event,'hint':'签到成功!','guest':result})

@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response
