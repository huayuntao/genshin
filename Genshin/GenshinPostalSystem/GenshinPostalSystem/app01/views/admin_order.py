# _*_ coding:utf-8 _*_
'''
    @FileName:admin_order.py
    @Author:Hao Chunbo
    @Data:18:36
    @Desc:这是一个描述
'''
from django.shortcuts import render, redirect
from django.utils import timezone

from app01 import models
from app01.utils.form import OrderForm
from app01.utils.pagination import Pagination


def admin_order_total(request):
    queryset = models.Order.objects.all().values('id', 'order_num', 'receiver__real_name', 'receive_addr', 'status')
    # for item in orders:
    #     queryset.append(
    #         {
    #             'order_num': item.order_num,
    #             'receiver__real_name': item.receiver.uname,
    #             'receive_addr': item.receive_addr,
    #             'status': item.get_status_display()
    #         }
    #     )
    # print(queryset)
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'admin_order_totail.html', context)


def admin_order_delete(request, the_id):
    models.Order.objects.filter(id=the_id).delete()
    return redirect('/admin/order/total/')


def admin_order_edit(request, the_id):
    if request.method == "GET":

        the_order_item = models.Order.objects.all().filter(id=the_id).values('id', 'receiver__uname','sender__uname',

                                                                             'send_addr','receive_addr', 'status').first()
        init_data = {
            'receiver_uname': the_order_item['receiver__uname'],
            'status': the_order_item['status'],
            'sender_uname': the_order_item['sender__uname'],
            'receive_addr': the_order_item['receive_addr'],
            'send_addr': the_order_item['send_addr'],
        }
        form = OrderForm(initial=init_data)
        return render(request, 'admin_order_add.html', {"form": form})
    form = OrderForm(data=request.POST)

    if form.is_valid():
        record_to_update = models.Order.objects.get(id=the_id)
        record_to_update.receiver_uname = form.cleaned_data['receiver_uname']
        record_to_update.status = form.cleaned_data['status']
        record_to_update.sender_uname = form.cleaned_data['sender_uname']
        record_to_update.receive_addr = form.cleaned_data['receive_addr']
        record_to_update.send_addr = form.cleaned_data['send_addr']
        record_to_update.save()
        return redirect('/admin/order/detail/{}'.format(the_id))
    return render(request, 'admin_order_add.html', {"form": form})


import shortuuid


def admin_order_add(request):
    if request.method == "GET":
        form = OrderForm()
        print(form)
        return render(request, 'admin_order_add.html', {"form": form})
    form = OrderForm(data=request.POST)

    if form.is_valid():
        models.Order.objects.create(order_num=shortuuid.uuid(),
                                    receiver=models.NormalUser.objects.all().filter(
                                        uname=form.cleaned_data['receiver_uname']).first(),
                                    sender=models.NormalUser.objects.all().filter(
                                        uname=form.cleaned_data['sender_uname']).first(),
                                    send_time=timezone.now(),
                                    send_addr=form.cleaned_data['send_addr'],
                                    receive_addr=form.cleaned_data['receive_addr'],
                                    status=form.cleaned_data['status']
                                    )

        return redirect('/admin/order/total/')
    return render(request, 'admin_order_add.html', {"form": form})


def admin_order_detail(request, the_id):
    the_order_item = models.Order.objects.all().filter(id=the_id).values('id', 'order_num'
           ,'receiver__uname' , 'receiver__real_name', 'receiver__phone_num', 'sender__uname','sender__real_name',
            'sender__phone_num', 'send_time', 'receive_time', 'send_addr',
            'receive_addr', 'status').first()
    the_order_status_set = models.OrderStatus.objects.all().filter(order_id=the_id).values(
        'time', 'courier__real_name', 'information'
    )
    context = {
        'the_order_item': the_order_item,
        'the_order_status_set': the_order_status_set
    }
    return render(request, 'order_detail.html', context)
