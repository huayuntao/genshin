from django.db import models


class NormalUser(models.Model):
    uname = models.CharField(max_length=64, verbose_name='用户名', unique=True)
    pwd = models.CharField(max_length=128, verbose_name='密码')
    real_name = models.CharField(max_length=16, verbose_name='真实姓名')
    phone_num = models.CharField(max_length=16, verbose_name='手机号')


class Courier(models.Model):
    uname = models.CharField(max_length=64, verbose_name='用户名', unique=True)
    pwd = models.CharField(max_length=128, verbose_name='密码')
    real_name = models.CharField(max_length=16, verbose_name='真实姓名')
    phone_num = models.CharField(max_length=16, verbose_name='电话号码')


class Admin(models.Model):
    uname = models.CharField(max_length=64, verbose_name='用户名')
    pwd = models.CharField(max_length=128, verbose_name='密码')


class Order(models.Model):
    order_num = models.CharField(max_length=32, verbose_name='订单号')
    receiver = models.ForeignKey(to='NormalUser', on_delete=models.CASCADE, verbose_name='接受者', related_name='sender')
    sender = models.ForeignKey(to='NormalUser', on_delete=models.CASCADE, verbose_name='发送者', related_name='receiver')
    send_time = models.DateTimeField(verbose_name='发送时间')
    receive_time = models.DateTimeField(null=True, blank=True, verbose_name='接受时间')
    send_addr = models.CharField(verbose_name='发件地点', max_length=128)
    receive_addr = models.CharField(verbose_name='收件地点', max_length=128)
    status_choices = (
        (1, "派送中"),
        (2, "已送达"),
        (3, "已取货"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)


class OrderStatus(models.Model):
    time = models.DateTimeField(verbose_name='时间')
    order = models.ForeignKey(to='Order', on_delete=models.CASCADE, verbose_name='订单')
    courier = models.ForeignKey(to='Courier', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='快递员')
    information = models.CharField(max_length=512, verbose_name='目前状况')
