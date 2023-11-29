"""
URL configuration for GenshinPostalSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app01.views.about_us import about_us
from app01.views.account import login, logout, register
from app01.views.admin_courier import admin_courier_edit, admin_courier_delete, admin_courier_add, admin_courier_list
from app01.views.admin_order import admin_order_total, admin_order_edit, admin_order_delete, admin_order_add, \
    admin_order_detail
from app01.views.admin_user import admin_user_list, admin_user_edit, admin_user_delete, admin_user_add
from app01.views.user import user_list_send, user_order_detail, user_list_receive, user_order_add, \
    user_personal_information_list, user_personal_information_edit, user_personal_information_change_password, \
    change_status_to_received
from app01.views.error404 import error404, error404_with_cause
from app01.views.courier import courier_personal_information_edit, courier_personal_information_change_password, \
    courier_personal_information_list, courier_home, courier_order_detail, change_status_to_served, \
    courier_add_information_to_order, courier_managed_order

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('admin/user/list/', admin_user_list),
    path('admin/user/edit/<int:the_id>/', admin_user_edit),
    path('admin/user/delete/<int:the_id>/', admin_user_delete),
    path('admin/user/add/', admin_user_add),
    path('admin/courier/list/', admin_courier_list),
    path('admin/courier/edit/<int:the_id>/', admin_courier_edit),
    path('admin/courier/delete/<int:the_id>/', admin_courier_delete),
    path('admin/courier/add/', admin_courier_add),
    path('admin/order/total/', admin_order_total),
    path('admin/order/edit/<int:the_id>/', admin_order_edit),
    path('admin/order/delete/<int:the_id>/', admin_order_delete),
    path('admin/order/add/', admin_order_add),
    path('admin/order/detail/<int:the_id>/', admin_order_detail),
    path('user/list/send', user_list_send),
    path('user/list/receive', user_list_receive),
    path('user/order/detail/<int:the_id>/', user_order_detail),
    path('user/order/add/', user_order_add),
    path('user/personal/information/list', user_personal_information_list),
    path('user/personal/information/edit', user_personal_information_edit),
    path('user/personal/information/change/password', user_personal_information_change_password),
    path('user/change/status/to/received/<int:order_id>/', change_status_to_received),
    path('courier/personal/information/list', courier_personal_information_list),
    path('courier/personal/information/edit', courier_personal_information_edit),
    path('courier/personal/information/change/password', courier_personal_information_change_password),
    path('courier/order/detail/<str:the_num>/', courier_order_detail),
    path('courier/change/status/to/served/<int:order_id>/', change_status_to_served),
    path('courier/add/information/to/order/<int:order_id>/', courier_add_information_to_order),
    path('courier/managed/order/', courier_managed_order),
    path('courier/home/', courier_home),
    path('logout/', logout),
    path('login/', login),
    path('register/', register),
    path('404/<str:exception>/', error404_with_cause),
    path('404/', error404),
    path('about-us/', about_us),
]
