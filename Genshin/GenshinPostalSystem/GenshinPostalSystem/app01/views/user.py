# _*_ coding:utf-8 _*_
'''
    @FileName:user.py
    @Author:Hao Chunbo
    @Data:21:58
    @Desc:这是一个描述
'''
import shortuuid
from django.db.models import Q
from django.utils import timezone

from app01 import models
from django.shortcuts import render, redirect, HttpResponse

from app01.utils.form import OrderFormUsedByUser, UserModelFormWithoutPassword, PasswordForm
from app01.utils.pagination import Pagination


def user_list_send(request):
    user_id = request.session.get("info")['id']
    queryset = models.Order.objects.all().values('id', 'order_num', 'receiver__real_name', 'receive_addr', 'status').filter(sender_id=user_id)
    the_trans_set = []
    for item in queryset:
        # print(item['sender'])
        # print(type(item))
        inf = models.OrderStatus.objects.all().values('information').filter(order_id=item['id']).order_by(
            '-time').first()
        the_trans_set.append({
            **item,
            'information': inf
        })
    return render(request, 'user_list_send.html', {'the_trans_set': the_trans_set})


def user_list_receive(request):
    # print(request.session.get("info"))
    user_id = request.session.get("info")['id']
    queryset = models.Order.objects.all().values('id', 'order_num', 'sender__real_name', 'receive_addr', 'status').filter(receiver_id=user_id)
    the_trans_set = []
    for item in queryset:
        # print(item['sender'])
        # print(type(item))
        inf = models.OrderStatus.objects.all().values('information').filter(order_id=item['id']).order_by(
            '-time').first()
        the_trans_set.append({
            **item,
            'information': inf
        })
    return render(request, 'user_list_receive.html', {'the_trans_set': the_trans_set})


def user_order_detail(request, the_id):
    user_id = request.session.get("info")['id']
    if not models.Order.objects.all().filter(id=the_id).filter(Q(receiver_id=user_id) | Q(sender_id=user_id)).exists():
        return redirect('/404/抱歉，这个订单与你无关，你无权访问')
    the_order_item = models.Order.objects.all().filter(id=the_id).values('id', 'order_num'
                                                                         , 'receiver__uname', 'receiver__real_name',
                                                                         'receiver__phone_num', 'sender__uname',
                                                                         'sender__real_name',
                                                                         'sender__phone_num', 'send_time',
                                                                         'receive_time', 'send_addr',
                                                                         'receive_addr', 'status').first()
    the_order_status_set = models.OrderStatus.objects.all().filter(order_id=the_id).values(
        'time', 'courier__real_name', 'information'
    )
    context = {
        'the_order_item': the_order_item,
        'the_order_status_set': the_order_status_set
    }
    return render(request, 'order_detail.html', context)

def user_order_add(request):
    user_id = request.session.get("info")['id']
    if request.method == "GET":
        form = OrderFormUsedByUser()
        print(form)
        return render(request, 'admin_order_add.html', {"form": form})
    form = OrderFormUsedByUser(data=request.POST)

    if form.is_valid():
        models.Order.objects.create(order_num=shortuuid.uuid(),
                                    receiver=models.NormalUser.objects.all().filter(
                                        uname=form.cleaned_data['receiver_uname']).first(),
                                    sender_id=user_id,
                                    send_time=timezone.now(),
                                    send_addr=form.cleaned_data['send_addr'],
                                    receive_addr=form.cleaned_data['receive_addr'],
                                    status=1
                                    )

        return redirect('/user/list/send')
    return render(request, 'admin_order_add.html', {"form": form})



def user_personal_information_list(request):
    user_id = request.session.get("info")['id']
    queryset = models.NormalUser.objects.all().values('uname', 'real_name', 'phone_num', 'id').filter(id=user_id).first()
    context = {
        "queryset": queryset,
        "role": request.session.get("info")['role']
    }
    print(context)
    return render(request, 'personal_information_list.html', context)

def user_personal_information_edit(request):
    user_id = request.session.get("info")['id']
    row_object = models.NormalUser.objects.all().filter(id=user_id).first()

    if request.method == "GET":
        form = UserModelFormWithoutPassword(instance=row_object)
        return render(request, 'personal_information_edit.html', {"form": form})

    form = UserModelFormWithoutPassword(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/personal/information/list')

    return render(request, 'personal_information_edit.html', {"form": form})

def user_personal_information_change_password(request):
    user_id = request.session.get("info")['id']
    if request.method == "GET":
        form = PasswordForm()
        return render(request, 'change_password.html', {"form": form})

    form = PasswordForm(data=request.POST)
    if form.is_valid():
        if form.cleaned_data['password'] != form.cleaned_data['again']:
            form.add_error("again", '两次密码不一致！')
            return render(request, 'change_password.html', {"form": form})
        obj_to_update = models.NormalUser.objects.get(id=user_id)
        obj_to_update.pwd = form.cleaned_data['password']
        obj_to_update.save()
        return redirect('/user/personal/information/list')
    return render(request, 'change_password.html', {"form": form})


def change_status_to_received(request, order_id):
    user_id = request.session.get("info")['id']
    order_to_update = models.Order.objects.get(id=order_id)
    if order_to_update.status == 2:
        order_to_update.status = 3
        order_to_update.save()
        new_order_status = models.OrderStatus(time=timezone.now(), order_id=order_id, information='用户已经取件')
        new_order_status.save()
        return redirect('/user/order/detail/{}'.format(order_id))
    else:
        return redirect('/404/订单为送达或者已经取件/')