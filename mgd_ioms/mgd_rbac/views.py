from django.shortcuts import render

from django.views.generic import TemplateView

from mgd_rbac.common import BreadcrumbMixin
from mgd_rbac.mixin import LoginRequiredMixin


class SystemView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):

    template_name = 'pc/mgd_rbac/rbac_index.html'
