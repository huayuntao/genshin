# _*_ coding:utf-8 _*_
'''
    @FileName:admin_courier.py
    @Author:Hao Chunbo
    @Data:17:17
    @Desc:这是一个描述
'''
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import CourierModelForm, CourierModelFormWithoutPassword

def admin_courier_list(request):
    queryset = models.Courier.objects.all().values('uname', 'real_name', 'phone_num', 'id')
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'admin_courier_list.html', context)

def admin_courier_delete(request, the_id):
    models.Courier.objects.filter(id=the_id).delete()
    return redirect('/admin/courier/list/')



def admin_courier_edit(request, the_id):
    row_object = models.Courier.objects.all().filter(id=the_id).first()
    if request.method == "GET":
        form = CourierModelFormWithoutPassword(instance=row_object)
        return render(request, 'admin_courier_edit.html', {"form": form})

    form = CourierModelFormWithoutPassword(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/courier/list')

    return render(request, 'admin_courier_edit.html', {"form": form})

def admin_courier_add(request):
    if request.method == "GET":
        form = CourierModelForm()
        print(form)
        return render(request, 'admin_courier_add.html', {"form": form})
    form = CourierModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/admin/courier/list/')
    return render(request, 'admin_courier_add.html', {"form": form})