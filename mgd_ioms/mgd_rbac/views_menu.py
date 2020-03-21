#__author:shixn 
#data:2020/3/16
from django.views.generic import ListView

from mgd_rbac.common import SandboxCreateView, BreadcrumbMixin, SandboxUpdateView
from mgd_rbac.mixin import LoginRequiredMixin
from mgd_rbac.models import Menu


class MenuCreateView(SandboxCreateView):
    model = Menu
    fields = '__all__'
    template_name = 'pc/mgd_rbac/menu/menu_form.html'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)


class MenuListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
    model = Menu

    context_object_name = 'menu_all'
    template_name = "pc/mgd_rbac/menu/menu_list.html"


class MenuUpdateView(SandboxUpdateView):
    model = Menu
    fields = '__all__'
    template_name = 'pc/mgd_rbac/menu/menu_update.html'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)