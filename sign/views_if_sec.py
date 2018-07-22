#!/usr/bin/env python  
# -*- coding: utf-8 -*-

""" 
@version: v1.0 
@author: 330mlcc 
@Software: PyCharm
@license: Apache Licence  
@Email   : mlcc330@hotmail.com
@contact: 3323202070@qq.com
@site:  
@software: PyCharm 
@file: views_if.py
@time: 18-7-21 下午5:23 
Description: 
"""

from django.http import JsonResponse
from sign.models import Event,Guest
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db.utils import IntegrityError
import time

# 添加发布会接口
def add_event(request):
    eid = request.POST.get('eid','')
    name = request.POST.get('name','')
    limit = request.POST.get('limit','')
    status = request.POST.get('status','')
    address = request.POST.get('address','')
    start_time = request.POST.get('start_time','')

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status':10021,'message':'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status':10022,'message':'event is already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status':10023,'message':'event name already exists'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid,name=name,limit=limit,address=address,status=int(status),start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error. It must in YYYY-MMM-DD HH:MM:SS format.'
        return JsonResponse({'status':10024,'message':error})

    return JsonResponse({'status':200,'message':'add event success.'})

# 查询发布会
def get_event_list(request):
    eid = request.GET.get('eid','')
    name = request.GET.get('name','')

    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty.'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success','date':event})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for result in results:
                event = {}
                event['name'] = result.name
                event['limit'] = result.limit
                event['status'] = result.status
                event['address'] = result.address
                event['start_time'] = result.start_time
                datas.append(event)

            return JsonResponse({'status': 200, 'message': 'success', 'date': datas})
    else:
        return JsonResponse({'status': 10022, 'message': 'query result is empty.'})

# 添加嘉宾
def add_guest(request):
    eid = request.POST.get('eid','')        # 关联发布会id
    realname = request.POST.get('realname','')
    phone = request.POST.get('phone','')
    email = request.POST.get('email','')

    if eid == '' or realname == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.get(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id is null.'})

    result = Event.objects.get(id=eid).status
    print(result)
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not available.'})

    event_limit = Event.objects.get(id=eid).limit       # 发布会限制人数
    guest_limit = Guest.objects.filter(event_id=eid)    # 发布会已经添加的人数

    if len(guest_limit) > event_limit:
        return JsonResponse({'status': 10024, 'message': 'event number is full.'})

    event_limit = Event.objects.get(id=eid).start_time  # 发布会时间
    etime = str(event_limit).split('.')[0]              #
    timeArray = time.strptime(etime,'%Y-%m-%d %H:%M:%S')
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())                         # 当前时间
    ntime = now_time.split('.')[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10025, 'message': 'event has started.'})

    try:
        Guest.objects.create(realname=realname,phone=int(phone),email=email,sign=0,event_id=int(eid))
    except IntegrityError:
        return JsonResponse({'status': 10026, 'message': 'The event guest phone number repeat.'})

    return JsonResponse({'status': 200, 'message': 'add guest is    successful!'})

# 查询嘉宾
def get_guest_list(request):
    eid = request.POST.get('eid','')
    phone = request.POST.get('phone','')

    if eid == '':
        return JsonResponse({'status': 10021, 'message': 'eid cannot be empyt'})

    if eid == '' and phone == '':
        dates = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for result in results:
                guest = {}
                guest['realname'] = result.realname
                guest['phone'] = result.phone
                guest['email'] = result.email
                guest['sign'] = result.sign
                dates.append(guest)
            return JsonResponse({'status': 200, 'message': 'succesful!','date':dates})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empyt'})

    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(phone=phone,event_id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empyt'})

        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign

            return JsonResponse({'status': 200, 'message': 'succesful!', 'date': guest})


# 嘉宾签到
def user_sign(request):
    # 用户签名+时间戳
    if request.method == 'POST':
        client_time = request.POST.get('time','')
        client_sign = request.POST.get('sign','')
    else:
        return 'error'

    if client_time == '' or client_sign == '':
        return 'sign is null5'

    eid = request.POST.get('eid','')        # 发布会id
    phone = request.POST.get('phone','')    # 嘉宾手机号

    # 发布会id和嘉宾手机号不能为空
    if eid == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter eeror.'})

    # 查询发布会判断发布会id是否存在
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id is null.'})

    # 判断发布会的状态是否为True
    result = Event.objects.get(id = eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not availiable.'})

    # 判断当前时间是否大于发布时间，如果大于，说明发布会已经开始，不允许签到
    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split('.')[0]
    timeArray = time.strptime(etime,'%Y-%m-%d %H:%M:%S')
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())
    ntime = now_time.split('.')[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10024, 'message': 'event has started'})

    # 判断嘉宾手机号是否存在
    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status': 10025, 'message': 'user phone is null.'})

    # 判断嘉宾的状态是否为已签到
    result = Guest.objects.filter(event_id=eid,phone=phone)
    if not result:
        return JsonResponse({'status': 10026, 'message': 'user did not participate in the conference.'})

    result = Guest.objects.get(event_id=eid,phone = phone).sign
    if result:
        return JsonResponse({'status': 10027, 'message': 'user has sign in.'})
    else:
        Guest.objects.filter(event_id=eid,phone=phone).update(sign='1')
        return JsonResponse({'status': 200, 'message': 'sign success.'})










