'''
存放form表单
'''
from django.core.exceptions import  ValidationError
from django import forms
from django.forms import widgets
class regform(forms.Form):
    username=forms.CharField(
        max_length=16,
        label='用户名',
        error_messages={
            'required':'姓名不能为空'
        },
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    password=forms.CharField(
        min_length=6,
        max_length=12,
        label='密码',
        error_messages={
            'min_length':'密码最小长度为6位',
            'required':'密码不能为空'
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
            # render_value=True,加入之后可以记住密码
    )
    re_pwd=forms.CharField(
        min_length=6,
        max_length=12,
        label='确认密码',
        error_messages={
            'min_length': '密码最小长度为6位',
            'required': '密码不能为空'
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    email=forms.EmailField(
        label='邮件',
        error_messages = {
               'invalid': '邮件格式不正确',
                'required': '邮件不能为空',
          },
        widget=widgets.EmailInput(attrs={'class': 'form-control'})
        )
    def clean(self):
        password=self.cleaned_data.get('password')
        re_pwd=self.cleaned_data.get('re_pwd')
        if re_pwd and password!=re_pwd:
            self.add_error('re_pwd',ValidationError('两次密码不一致'))
        else:
            return self.cleaned_data