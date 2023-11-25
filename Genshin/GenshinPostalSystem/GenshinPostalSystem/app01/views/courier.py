# _*_ coding:utf-8 _*_
'''
    @FileName:courier.py
    @Author:Hao Chunbo
    @Data:10:57
    @Desc:这是一个描述
'''

from django.shortcuts import render, redirect
from django.utils import timezone

from app01 import models
from app01.utils.form import UserModelFormWithoutPassword, PasswordForm, OrderStatusModelForm
from app01.utils.pagination import Pagination


def courier_personal_information_list(request):
    user_id = request.session.get("info")['id']
    queryset = models.Courier.objects.all().values('uname', 'real_name', 'phone_num', 'id').filter(id=user_id).first()
    context = {
        "queryset": queryset,
        "role": request.session.get("info")['role']
    }
    print(context)
    return render(request, 'personal_information_list.html', context)

def courier_personal_information_edit(request):
    user_id = request.session.get("info")['id']
    row_object = models.Courier.objects.all().filter(id=user_id).first()

    if request.method == "GET":
        form = UserModelFormWithoutPassword(instance=row_object)
        return render(request, 'personal_information_edit.html', {"form": form})

    form = UserModelFormWithoutPassword(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/courier/personal/information/list')

    return render(request, 'personal_information_edit.html', {"form": form})

def courier_personal_information_change_password(request):
    user_id = request.session.get("info")['id']
    if request.method == "GET":
        form = PasswordForm()
        return render(request, 'change_password.html', {"form": form})

    form = PasswordForm(data=request.POST)
    if form.is_valid():
        if form.cleaned_data['password'] != form.cleaned_data['again']:
            form.add_error("again", '两次密码不一致！')
            return render(request, 'change_password.html', {"form": form})
        obj_to_update = models.Courier.objects.get(id=user_id)
        obj_to_update.pwd = form.cleaned_data['password']
        obj_to_update.save()
        return redirect('/courier/personal/information/list')
    return render(request, 'change_password.html', {"form": form})

def courier_add_information_to_order(request, order_id):
    user_id = request.session.get("info")['id']
    if request.method == "GET":
        form = OrderStatusModelForm()
        return render(request, 'courier_add_information_to_order.html', {"form": form})

    form = OrderStatusModelForm(data=request.POST)
    if form.is_valid():
        form.instance.time=timezone.now()
        form.instance.order_id = order_id
        form.instance.courier_id = user_id
        form.save()
        order_num = models.Order.objects.all().filter(id=order_id).values('order_num').first()
        print(order_num['order_num'])
        return redirect('/courier/order/detail/{}'.format(order_num['order_num']))
    return render(request, 'change_password.html', {"form": form})

def change_status_to_served(request, order_id):
    user_id = request.session.get("info")['id']
    order_to_update = models.Order.objects.get(id=order_id)
    if order_to_update.status == 1:
        order_to_update.status = 2
        order_to_update.save()
        new_order_status = models.OrderStatus(time=timezone.now(), order_id=order_id, courier_id=user_id, information='我已将快递送达，请及时取件')
        new_order_status.save()
        return redirect('/courier/order/detail/{}'.format(order_id))
    else:
        return redirect('/404/订单已经送达或者已经被取走/')

def courier_home(request):
    return render(request, 'courier_home.html')

def courier_order_detail(request, the_num):
    the_order_item = models.Order.objects.all().filter(order_num=the_num).values('id', 'order_num'
                                                                         , 'receiver__uname', 'receiver__real_name',
                                                                         'receiver__phone_num', 'sender__uname',
                                                                         'sender__real_name',
                                                                         'sender__phone_num', 'send_time',
                                                                         'receive_time', 'send_addr',
                                                                         'receive_addr', 'status').first()
    if not the_order_item:
        return redirect('/404/未找到这一个快递/')
    the_id = the_order_item['id']
    the_order_status_set = models.OrderStatus.objects.all().filter(order_id=the_id).values(
        'time', 'courier__real_name', 'information'
    )
    context = {
        'the_order_item': the_order_item,
        'the_order_status_set': the_order_status_set
    }
    return render(request, 'order_detail.html', context)


def courier_managed_order(request):
    user_id = request.session.get("info")['id']
    queryset = models.OrderStatus.objects.all().filter(courier_id=user_id).values('order__order_num', 'order__receive_addr', 'order__receiver__real_name', 'order__status', 'information').order_by('-time')
    print(queryset)
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'courier_managed_order.html', context)
