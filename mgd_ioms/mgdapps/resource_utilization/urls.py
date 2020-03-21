from django.urls import path

from mgdapps.resource_utilization import views

urlpatterns = [
    path('screen/', views.screen),
    path("usage/", views.get_resource_utilization),
    path("get_history/", views.get_history),
    path("get_utilization_info/", views.get_utilization_info),
    path("get_group_host/", views.get_group_host),
    path("get_host_ip/", views.get_host_ip),
    path("get_list_host/", views.get_list_host),
    path('host_detailspage/', views.host_detailspage),  # 主机详情页面
    path('host_page/', views.host_page),  # 主机详情页面

]
