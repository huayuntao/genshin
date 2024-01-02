# _*_ coding:utf-8 _*_
'''
    @FileName:error404.py
    @Author:Hao Chunbo
    @Data:0:02
    @Desc:这是一个描述
'''
from django.shortcuts import render


def error404_with_cause(request, exception):
    return render(request, '404.html',{
        'exception': exception
    })

def error404(request):
    return render(request, '404.html',{
        'exception': '我们遇到了原宇宙中无法解决的问题'
    })