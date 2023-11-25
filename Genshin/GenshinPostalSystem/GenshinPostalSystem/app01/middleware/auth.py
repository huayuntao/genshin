# _*_ coding:utf-8 _*_
'''
    @FileName:auth.py
    @Author:Hao Chunbo
    @Data:23:59
    @Desc:这是一个描述
'''
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
import re


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 调试语句
        # return
        info_dict = request.session.get("info")
        if request.path_info in ["/"]:
            return redirect('/login/')
        if request.path_info in ["/login/", "/logout/", "/register/"]\
                or re.match(r'^/404', request.path_info):
            return
        if not info_dict:
            return redirect('/login/')
        if info_dict['role'] == '1':
            if re.match(r'^/user', request.path_info):
                return
            else:
                return redirect('/404/越权访问！')
        elif info_dict['role'] == '2':
            if re.match(r'^/courier', request.path_info):
                return
            else:
                return redirect('/404/越权访问！')
        else:
            if re.match(r'^/admin', request.path_info):
                return
            else:
                return redirect('/404/越权访问！')
        print(info_dict)
