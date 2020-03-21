import json
import time
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here
from django.views import View
from django.core.paginator import Paginator
from mgd_ioms.settings import ZABBIX_API_URL_60, ZABBIX_USERNAME_60, ZABBIX_PASSWORD_60, zabbix_header
from mgdapps.config_manage.models import MonitorItem, EquipmentClassification
from mgdapps.utils import request_body, user_login, get_history_data


class Item(View):
    """监控项管理"""
    def get(self, request):
        """
        获取监控项
        :param request: 请求对象
        :return: 监控项数据
        """
        token = user_login(ZABBIX_API_URL_60, ZABBIX_USERNAME_60, ZABBIX_PASSWORD_60)
        page = request.GET.get('page')
        hostid = request.GET.get('hostid')
        # 获取到该设备对象
        id = EquipmentClassification.objects.get(host_id=hostid)
        # 查询数据
        items = MonitorItem.objects.filter(equipment_id_id=id)
        # 创建分页实例
        paginator = Paginator(items, 4)
        # 获取指定页码的数据
        page_data = paginator.page(page)
        # 获取所有页面数据总量
        value = Paginator.count
        # 创建一个字典来存放监控项所对应的键值
        item_dict = dict()
        # 创建一个字典来存放监控指标所对应的图形展示类型
        type_dict = dict()
        for i in page_data:
            item_dict[i.item] = i.item_key
            type_dict[i.item] = i.graph_type
        # 创建一个字典存放返回数据
        return_dict = dict()
        for i in item_dict:
            # 创建一个字典存放历史数据 时间:数据
            history_dict = dict()
            item_list = request_body(hostid, item_dict[i], token, ZABBIX_API_URL, zabbix_header)
            if item_list:
                itemid = i['itemid']
                history_list = get_history_data(token, itemid, ZABBIX_API_URL)
                for index, item in enumerate(history_list):
                    # 转换时间戳
                    timeArray = time.localtime(int(item['clock']))
                    historica_time = time.strftime("%m-%d", timeArray)
                    value = round(float(item['value']) / 1000, 2)  # 拿到历史值
                    history_dict[historica_time] = value
                # 返回监控指标所对应的图表展示类型
                history_dict['graph_type'] = type_dict[i]
                return_dict[i] = history_dict
            else:
                return_dict[i] = {}
        # 构造返回数据
        # 数据量总数
        return_dict['total'] = value
        return HttpResponse(json.dumps(return_dict, ensure_ascii=False), content_type="application/json,charset=utf-8")
