# _*_ coding:utf-8 _*_
'''
    @FileName:account.py
    @Author:Hao Chunbo
    @Data:17:17
    @Desc:这是一个描述
'''
from django import forms
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.encrypt import md5
from app01.utils.form import RegisterForm

role_choices = (
    (1, '用户'),
    (2, '快递员'),
    (3, '管理员'),
)


class LoginForm(forms.Form):
    username = forms.CharField(max_length='64', label='用户名', widget=forms.TextInput)
    password = forms.CharField(max_length='128', label='密码', widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=role_choices, label='角色')

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    info_dict = request.session.get("info")
    if info_dict:
        if info_dict['role'] == '1':
            return redirect('/user/list/send')
        elif info_dict['role'] == '2':
            return redirect('/courier/home')
        else:
            return redirect('/admin/user/list')

    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    the_id = 0
    if form.is_valid():
        obtained = {
            'uname': form.cleaned_data['username'],
            'pwd': form.cleaned_data['password'],
        }
        ok = False
        # print(form.cleaned_data['role'])
        if form.cleaned_data['role'] == '1':
            ok = models.NormalUser.objects.filter(uname=obtained['uname'], pwd=obtained['pwd']).exists()
            the_id = models.NormalUser.objects.filter(uname=obtained['uname'], pwd=obtained['pwd']).values('id').first()
            uname = models.NormalUser.objects.filter(uname=obtained['uname'], pwd=obtained['pwd']).values('uname').first()
        elif form.cleaned_data['role'] == '2':
            ok = models.Courier.objects.filter(uname=obtained['uname'], pwd=obtained['pwd']).exists()
            the_id = models.Courier.objects.filter(uname=obtained['uname'], pwd=obtained['pwd']).values('id').first()
            uname = models.Courier.objects.filter(uname=obtained['uname'], pwd=obtained['pwd']).values('uname').first()
        else:
            ok = models.Admin.objects.filter(uname=obtained['uname'], pwd=obtained['pwd']).exists()
            the_id = models.Admin.objects.filter(uname=obtained['uname'], pwd=obtained['pwd']).values('id').first()
            uname = models.Admin.objects.filter(uname=obtained['uname'], pwd=obtained['pwd']).values(
                'uname').first()
        if not ok:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；

        # print(type(the_id))
        request.session["info"] = {'id': the_id['id'], 'role': form.cleaned_data['role'], 'uname': uname['uname']}
        print(request.session["info"])
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        info_dict = request.session.get("info")
        if info_dict:
            if info_dict['role'] == '1':
                return redirect('/user/list/send')
            elif info_dict['role'] == '2':
                return redirect('/courier/home')
            else:
                return redirect('/admin/user/list')

    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect('/login/')


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        if form.cleaned_data['again'] != form.cleaned_data['pwd']:
            print(form.cleaned_data)
            form.add_error('again', '两次密码输入不一致！')
            return render(request, 'register.html', {'form': form})
        form.save()
        return redirect('/login')
    return render(request, 'register.html', {'form': form})