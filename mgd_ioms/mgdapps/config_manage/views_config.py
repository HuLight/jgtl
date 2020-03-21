#   @author:HuKai
#   @time:2020-03-19 17:07
import json
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from mgdapps.config_manage import get_response, get_auth
from mgdapps.config_manage.models import EquipmentClassification, HostGroup, MonitorItem

# Create your views here.
auth = get_auth()
host_model = EquipmentClassification()
group_model = HostGroup()


def get_groups():
    """获取群组信息,names:主机信息"""
    if auth:
        data = {"jsonrpc": "2.0", "auth": auth, "id": 1, "method": "hostgroup.get",
                "params": {
                    "output": ['group', "name"],
                },
                }
        return get_response(data)
    else:
        #   没有获取身份令牌的原因
        return


def get_hosts():
    """获取主机信息"""
    if auth:
        data = {'jsonrpc': '2.0',
                'method': 'host.get',
                'params': {
                    'output': ["hostid", "host", ],
                },
                'auth': auth,
                'id': '1'
                }
        print(get_response(data))
        return get_response(data)
    else:
        #   防止身份令牌获取不到返回状态码
        return


def display_host_groups(request):
    """展示主机和群组群组"""
    group_name = request.GET.get('group')
    if not group_name:
        groups = [group.get('name') for group in get_groups()]  # 数据库没有数据做出响应

        return render(request, 'pc/config_host_group.html', context={
            "groups": groups,
            })
    else:
        db_hosts = EquipmentClassification.objects.all()
        if not db_hosts:
            return JsonResponse({'status': 2})
        else:

            hosts = [[host.equipment,host.subject] for host in db_hosts.order_by('-sort_no')]
            return render(request,'pc/select_equipment.html',context={'hosts':hosts,'group':group_name})


def group_sync(request):
    """zabbix同步数据到mysql"""

    querysetlist = []
    zabbix_groups = [(group.get('groupid'), group.get('name')) for group in get_groups()]  # zabbix群组名称
    db_groups = HostGroup.objects.all()
    if db_groups:
        group_list = [(str(group.group_id), group.name) for group in db_groups]
        #   差集
        subtract = set(zabbix_groups) - set(group_list)
        if not subtract:
            #   zabbix群组和数据库数据相同或少于mysql数据库
            return JsonResponse({'status': 2})
        else:
            for data in subtract:
                querysetlist.append(HostGroup(group_id=data[0], name=data[1]))
            # 批量创建对象插入数据库
            HostGroup.objects.bulk_create(querysetlist)
            return JsonResponse({"status": 1})
    else:
        for group in zabbix_groups:
            querysetlist.append(HostGroup(group_id=group[0], name=group[1]))
        HostGroup.objects.bulk_create(querysetlist)
        return JsonResponse({'status': 1})


def config_ralationship(request):
    """前端提交一个群组和对应的主机,设置mysql的对应关系"""

    if request.method == 'POST':
        body = request.body
        if not body:
            #   前端做提交控制，后端做body为空判断
            return JsonResponse({"status": 3})
        else:
            response = json.loads(body)
            #   获取所有群组
            group = response.get('group')
            db_group = HostGroup.objects.get(name=group)
            hosts = response.get('hosts')
            #   获取所有主机分类的数据库id
            ids = [db_id.id for db_id in EquipmentClassification.objects.filter(equipment__in=hosts)]
            db_group.host.add(*ids)
            return JsonResponse({'status': 1})


class ConfigItem(View):
    """监控指标操作"""

    def get(self, reqeust):
        item_ado = [key.name for key in MonitorItem._meta.fields]
        db_items = [(item.id, item.item, item.item_key, item.graph_type, item.sorted_no) for item in
                    MonitorItem.objects.all()]
        return JsonResponse({'fields': item_ado, 'items': db_items})

    def post(self, request):
        """增加监控指标"""
        response = request.body
        if not response:
            return JsonResponse({'status': 3})
        else:
            items = json.loads(response).get('items')
            #   目前单条添加
            MonitorItem.objects.create(item=items['item'], item_key=items['item_key'], graph_type=items['graph_type'],
                                       sorted_no=items['sorted_no'], equipment_id=items['equipment_id'])
            return JsonResponse({'status': 1})

    def delete(self, request):
        """删除监控指标"""

        response = request.body
        if not response:
            return JsonResponse({'status': 3})
        else:
            id = json.loads(response).get('id')
            MonitorItem.objects.filter(id=id).delete()
            return JsonResponse({'status': 1})

    def put(self, request):
        """更新监控指标"""
        response = request.body
        if not response:
            return JsonResponse({'status': 3})
        else:
            id = json.loads(response).get('id')
            item = json.loads(response).get('items')

            MonitorItem.objects.filter(id=id).update(**item)
            return JsonResponse({'status': 1})

def get_equipments(request):
    """返回json格式 设备数据"""

    if request.method == 'POST':
        response = request.body
        if not response:
            return JsonResponse({'status':3})
        else:
            subject = json.loads(response)
            equipments = [sub.equipment for sub in EquipmentClassification.objects.filter(subject=subject.get('subject'))]
            return JsonResponse({'equipments':equipments})