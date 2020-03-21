#__author:shixn 
#data:2020/3/13
from django.contrib.auth.decorators import login_required

"""
页面访问限制的实现需求：
- 用户登录系统才可以访问某些页面 - 如果用户没有登陆而直接访问就会跳转到登陆界面 
- 用户在跳转的登陆页面完成登陆后，自动访问跳转前的访问地址
"""

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **init_kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**init_kwargs)
        return login_required(view)