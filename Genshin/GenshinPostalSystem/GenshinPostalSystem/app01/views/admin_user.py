# _*_ coding:utf-8 _*_
'''
    @FileName:admin_user.py
    @Author:Hao Chunbo
    @Data:17:17
    @Desc:这是一个描述
'''
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, UserModelFormWithoutPassword


def admin_user_list(request):
    queryset = models.NormalUser.objects.all().values('uname', 'real_name', 'phone_num', 'id')
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'admin_user_list.html', context)

def admin_user_delete(request, the_id):
    models.NormalUser.objects.filter(id=the_id).delete()
    return redirect('/admin/user/list/')



def admin_user_edit(request, the_id):
    row_object = models.NormalUser.objects.all().filter(id=the_id).first()

    if request.method == "GET":
        form = UserModelFormWithoutPassword(instance=row_object)
        return render(request, 'admin_user_edit.html', {"form": form})

    form = UserModelFormWithoutPassword(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/user/list')

    return render(request, 'admin_user_edit.html', {"form": form})

def admin_user_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'admin_user_add.html', {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/user/list/')
    return render(request, 'admin_user_add.html', {"form": form})

