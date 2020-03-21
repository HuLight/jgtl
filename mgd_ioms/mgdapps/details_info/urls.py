from django.urls import path

from mgdapps.details_info import views

urlpatterns = [
    path("index/", views.get_index),
    path('get_detailspage_info/', views.get_detailspage_info),  # 获取主机监控信息
    path('detailspage/', views.detailspage),  # 详情页面主页
    path('get_information_bar/', views.get_information_bar),  # 获取左侧bar条
    path('network_detailspage/', views.network_detailspage),  # 网络详情页面
    path('get_network_equipment_info/', views.get_network_equipment_info),  # 获取网络设备信息
    path('information/', views.information),  # 网口信息页面
    path('get_port_info/', views.get_port_info),  # 网口信息方法
    path('get_admin_list/', views.get_admin_list),  # 管理员列表
    path('get_admin_role/', views.get_admin_role),  # 角色管理
    path('get_admin_cate/', views.get_admin_cate),  # 权限分类
    path('get_admin_rule/', views.get_admin_rule),  # 权限管理
    path('get_template_data/', views.get_template_data),  # 测试模板
    path('get_template_page/', views.get_template_page)
]