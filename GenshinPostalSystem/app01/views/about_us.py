# _*_ coding:utf-8 _*_
'''
    @FileName:about_us.py
    @Author:Hao Chunbo
    @Data:23:23
    @Desc:这是一个描述
'''
from django.shortcuts import redirect, render


def about_us(request):
    return render(request, 'about_us.html')
