from django.urls import path
from mgdapps.config_manage.views import Item
from mgdapps.config_manage import views_config
from mgdapps.config_manage.views_config import ConfigItem

urlpatterns = [
    path('config/item/', Item.as_view()),
    path('config/group/', views_config.display_host_groups, name='display_host_groups'),
    path('config/sync/', views_config.group_sync, name='sync'),
    path('config/ralationship/', views_config.config_ralationship, name='conifg_ralationship'),
    path('config/item/', ConfigItem.as_view(), name='configitem'),
    path('config/equipment/',views_config.get_equipments,name='get_equipments'),
]
