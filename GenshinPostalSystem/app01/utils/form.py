from django.shortcuts import redirect

from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from app01.utils.bootstrap import BootStrapModelForm
from django.core.exceptions import ValidationError

from app01.utils.encrypt import md5


class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.NormalUser
        fields = ['uname', 'pwd', 'real_name', 'phone_num']

    def clean_pwd(self):
        pwd = self.cleaned_data.get("pwd")
        return md5(pwd)


class UserModelFormWithoutPassword(BootStrapModelForm):
    class Meta:
        model = models.NormalUser
        fields = ['uname', 'real_name', 'phone_num']


class CourierModelForm(BootStrapModelForm):
    class Meta:
        model = models.Courier
        fields = ['uname', 'pwd', 'real_name', 'phone_num']

    def clean_pwd(self):
        pwd = self.cleaned_data.get("pwd")
        return md5(pwd)


class CourierModelFormWithoutPassword(BootStrapModelForm):
    class Meta:
        model = models.Courier
        fields = ['uname', 'real_name', 'phone_num']


class OrderForm(forms.Form):
    receiver_uname = forms.CharField(max_length=64, label='收件人用户名')
    sender_uname = forms.CharField(max_length=64, label='发件人用户名')
    send_addr = forms.CharField(max_length=128, label='发件地址')
    receive_addr = forms.CharField(max_length=128, label='收件地址')
    status = forms.ChoiceField(choices=models.Order.status_choices, label='邮件状态')

    def clean_sender_uname(self):
        name = self.cleaned_data['sender_uname']
        if models.NormalUser.objects.filter(uname=name).exists():
            return name
        else:
            raise ValidationError('发件人不存在')

    def clean_receiver_uname(self):
        name = self.cleaned_data['receiver_uname']
        if models.NormalUser.objects.filter(uname=name).exists():
            return name
        else:
            raise ValidationError('收件人不存在')


class OrderFormUsedByUser(forms.Form):
    receiver_uname = forms.CharField(max_length=64, label='收件人用户名')
    send_addr = forms.CharField(max_length=128, label='发件地址')
    receive_addr = forms.CharField(max_length=128, label='收件地址')

    def clean_receiver_uname(self):
        name = self.cleaned_data['receiver_uname']
        if models.NormalUser.objects.filter(uname=name).exists():
            return name
        else:
            raise ValidationError('收件人不存在')


class PasswordForm(forms.Form):
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    again = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_again(self):
        pwd = self.cleaned_data.get("again")
        return md5(pwd)


class OrderStatusModelForm(BootStrapModelForm):
    class Meta:
        model = models.OrderStatus
        fields = ['information']


class RegisterForm(BootStrapModelForm):
    class Meta:
        model = models.NormalUser
        fields = '__all__'
    pwd = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    again = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    def clean_pwd(self):
        pwd = self.cleaned_data.get("pwd")
        return md5(pwd)

    def clean_again(self):
        pwd = self.cleaned_data.get("again")
        return md5(pwd)
