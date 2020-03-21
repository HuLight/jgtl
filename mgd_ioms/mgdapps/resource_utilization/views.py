import json
import time
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from pypinyin import pinyin

from mgd_ioms.settings import ZABBIX_USERNAME, ZABBIX_PASSWORD, ZABBIX_API_URL
from .models import Basic_Info, Utilization
from mgdapps.utils import zabbix_api, get_hostlist, send_data, user_login, get_itemid


def screen(request):
    return render(request, '../frontend/pc/screen_one.html')


def host_page(request):
    """
    主机监控详情页
    """
    return render(request, '../frontend/pc/host_page.html')


def host_detailspage(request):
    """
    主机监控详情页
    """
    return render(request, '../frontend/pc/host_detailspage.html')


def get_resource_utilization(request):
    """
    获取资源利用率页面
    :param request:
    :return:
    """
    return render(request, '../frontend/pc/resource_utilization.html')


def get_history(request):
    """
    获取每台主机的90天内历史记录cpu，内存，磁盘的使用率,并存入数据库
    :param request:
    :return:
    """
    url = ZABBIX_API_URL
    header = {"Content-Type": "application/json-rpc"}
    token = user_login(url, ZABBIX_USERNAME, ZABBIX_PASSWORD)
    # 调用get_itemid()获取itemid_dict
    # cpu使用率的搜索键值
    key = "system.cpu.util"
    cpu_dict = get_itemid(key, token, url, header)
    # cpu空闲比
    key = "system.cpu.util[,idle]"
    cpu_dict1 = get_itemid(key, token, url, header)
    for i in cpu_dict1:
        if i in cpu_dict:
            del cpu_dict[i]
    # 内存使用率的搜索键值
    key = "vm.memory.size[pavailable]"
    memory_dict = get_itemid(key, token, url, header)
    key = "vm.memory.util"
    memory_dict1 = get_itemid(key, token, url, header)
    for i in memory_dict1:
        memory_dict[i] = memory_dict1[i]
    # 创建字典存放主机cpu使用率的信息
    host_utili_dict = dict()
    # 获取linux系统主机的cpu使用率
    for i in cpu_dict1:
        # 创建一个字典存放cpu的最大值，最小值，平均值
        cpu_value = dict()
        # sum用来计算平均值
        sum = 0
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 0,
                "itemids": cpu_dict1[i],
                "sortfield": "clock",
                "sortorder": "DESC",
                "time_from": int(time.time() - 7776000),
                "time_till": int(time.time()),
            },
            "auth": token,
            "id": 1
        }
        history_list = zabbix_api(url, header, data)
        value_dict = dict()
        for j in history_list:
            value_dict[j['clock']] = j['value']
        value_list = sorted(value_dict.items(), key=lambda item: item[1])
        for k in value_list:
            sum += float(value_list[0][1])
        cpu_value['cpu_value_avg'] = round(100 - sum / len(value_list), 2)
        cpu_value['cpu_value_max'] = round(100 - float(value_list[0][1]), 2)
        cpu_value['cpu_max_clock'] = value_list[0][0]
        cpu_value['cpu_value_min'] = round(100 - float(value_list[-1][1]), 2)
        cpu_value['cpu_min_clock'] = value_list[-1][0]
        host_utili_dict[i] = cpu_value
    for i in cpu_dict:
        # 创建一个字典存放cpu的最大值，最小值，平均值
        cpu_value = dict()
        # sum用来计算平均值
        sum = 0
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 0,
                "itemids": cpu_dict[i],
                "sortfield": "clock",
                "sortorder": "DESC",
                "time_from": int(time.time() - 7776000),
                "time_till": int(time.time()),
            },
            "auth": token,
            "id": 1
        }
        history_list = zabbix_api(url, header, data)
        value_dict = dict()
        for j in history_list:
            value_dict[j['clock']] = j['value']
        value_list = sorted(value_dict.items(), key=lambda item: item[1])
        for k in value_list:
            sum += float(value_list[0][1])
        cpu_value['cpu_value_avg'] = round(sum / len(value_list), 2)
        cpu_value['cpu_value_min'] = round(float(value_list[0][1]), 2)
        cpu_value['cpu_max_clock'] = value_list[0][0]
        cpu_value['cpu_value_max'] = round(float(value_list[-1][1]), 2)
        cpu_value['cpu_min_clock'] = value_list[-1][0]
        host_utili_dict[i] = cpu_value

    # 创建字典存放主机内存使用率的信息
    host_mem_dict = dict()
    for i in memory_dict:
        # 创建一个字典存放内存的最大值，最小值，平均值
        mem_value = dict()
        # sum用来计算平均值
        sum = 0
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 0,
                "itemids": memory_dict[i],
                "sortfield": "clock",
                "sortorder": "DESC",
                "time_from": int(time.time() - 7776000),
                "time_till": int(time.time()),
            },
            "auth": token,
            "id": 1
        }
        history_list = zabbix_api(url, header, data)
        value_dict = dict()
        for j in history_list:
            value_dict[j['clock']] = j['value']
        value_list = sorted(value_dict.items(), key=lambda item: item[1])
        for k in value_list:
            sum += float(value_list[0][1])
        mem_value['mem_value_avg'] = round(sum / len(value_list), 2)
        mem_value['mem_value_min'] = round(float(value_list[0][1]), 2)
        mem_value['mem_max_clock'] = value_list[0][0]
        mem_value['mem_value_max'] = round(float(value_list[-1][1]), 2)
        mem_value['mem_min_clock'] = value_list[-1][0]
        host_mem_dict[i] = mem_value
    # 创建字典存放主机基本信息
    basic_info = dict()
    host_list = get_hostlist(token, url, header)
    for i in host_list:
        # 获取主机的cpu型号，内存大小，磁盘大小，磁盘已使用，磁盘使用率
        # 构建zabbix请求体,获取主机内存的大小
        key = "vm.memory.size[total]"
        memory_list = send_data(i, key, token, url, header)
        if len(memory_list) == 0:
            i['memory_size'] = 0
        else:
            i['memory_size'] = str(round(float(memory_list[0]['lastvalue']) / 1024 ** 3))
        # 获取主机磁盘的大小
        key = "vfs.fs.size[/,total]"
        disk_list = send_data(i, key, token, url, header)
        # 黄羊web服务
        if len(disk_list) == 0:
            key = "vfs.fs.size[C:,total]"
            key1 = "vfs.fs.size[D:,total]"
            disk_list = send_data(i, key, token, url, header)
            disk_list1 = send_data(i, key1, token, url, header)
            if len(disk_list) == 0 and len(disk_list1) == 0:
                i['disk_size'] = 0
            else:
                i['disk_size'] = round(
                    (float(disk_list[0]['lastvalue']) + float(disk_list1[0]['lastvalue'])) / 1024 ** 3)
        else:
            i['disk_size'] = round(float(disk_list[0]['lastvalue']) / 1024 ** 3)
        # 获取cpu的个数
        key = "system.cpu.num"
        cpu_list = send_data(i, key, token, url, header)
        if len(cpu_list) == 0:
            i['cpu_num'] = 0
        else:
            i['cpu_num'] = cpu_list[0]['lastvalue']
        # 获取磁盘使用率
        key = "vfs.fs.size[/,pused]"
        used_list = send_data(i, key, token, url, header)
        if len(used_list) == 0:
            # 获取黄羊机器磁盘使用率
            key = "vfs.fs.size[C:,pused]"
            used_list = send_data(i, key, token, url, header)
            if len(used_list) == 0:
                i['disk_used_percent'] = 0
                i['disk_clock'] = 0
            else:
                i['disk_used_percent'] = used_list[0]['lastvalue']
                i['disk_clock'] = used_list[0]['lastclock']
        else:
            i['disk_used_percent'] = used_list[0]['lastvalue']
            i['disk_clock'] = used_list[0]['lastclock']
        # 通过hostid获取主机组信息
        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": ["name"],
                "hostids": i['hostid'],
            },
            "auth": token,
            "id": 1
        }
        # 返回响应
        group_list = zabbix_api(url, header, data)
        i['group_id'] = group_list[0]['groupid']
        i['group_name'] = group_list[0]['name']
        basic_info[i['hostid']] = i
    # 将内存的使用率情况和磁盘的使用率情况添加到host_utili_dict;
    for i in host_utili_dict:
        host_utili_dict[i]['mem_value_avg'] = host_mem_dict[i]['mem_value_avg']
        host_utili_dict[i]['mem_value_min'] = host_mem_dict[i]['mem_value_min']
        host_utili_dict[i]['mem_value_max'] = host_mem_dict[i]['mem_value_max']
        host_utili_dict[i]['mem_max_clock'] = host_mem_dict[i]['mem_max_clock']
        host_utili_dict[i]['disk_clock'] = basic_info[i]['disk_clock']
        host_utili_dict[i]['disk_used'] = basic_info[i]['disk_used_percent']

    for i in basic_info:
        # 向数据库基本信息表中添加数据
        try:
            info = Basic_Info(clock=int(time.time()), groupid=basic_info[i]['group_id'],
                              group_name=basic_info[i]['group_name'],
                              host_id=i, host=basic_info[i]['host'], host_name=basic_info[i]['name'],
                              status=basic_info[i]['status'], ip_addr=basic_info[i]['interfaces'][0]['ip'],
                              cpu_num=basic_info[i]['cpu_num'], memory_size=basic_info[i]['memory_size'],
                              disk_size=basic_info[i]['disk_size'])
            info.save()

        except Exception as err:
            print("err2", err)
            return HttpResponse(json.dumps({"msg": "获取失败"}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
    for i in host_utili_dict:
        try:
            # 向数据库使用率表中添加数据
            utili = Utilization(clock=int(time.time()), host_id_id=i, cpu_clock=host_utili_dict[i]['cpu_max_clock'],
                                cpu_value_min=host_utili_dict[i]['cpu_value_min'],
                                cpu_value_max=host_utili_dict[i]['cpu_value_max'],
                                cpu_value_avg=host_utili_dict[i]['cpu_value_avg'],
                                mem_clock=host_utili_dict[i]['mem_max_clock'],
                                mem_value_min=host_utili_dict[i]['mem_value_min'],
                                mem_value_max=host_utili_dict[i]['mem_value_max'],
                                mem_value_avg=host_utili_dict[i]['mem_value_avg'],
                                disk_clock=host_utili_dict[i]['disk_clock'],
                                disk_used=host_utili_dict[i]['disk_used'])
            utili.save()
        except Exception as err:
            print("err3", err)
            return HttpResponse(json.dumps({"msg": "获取失败"}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
    return HttpResponse(json.dumps({"msg": "获取成功"}, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_utilization_info(request):
    """从数据库获取主机信息"""
    cpu_value = request.GET['cpuValue']
    memory_value = request.GET['memoryValue']
    if cpu_value:
        cpu_value = int(cpu_value)
    else:
        cpu_value = 0
    if memory_value:
        memory_value = int(memory_value)
    else:
        memory_value = 0

    selectGroup = request.GET['selectGroup']
    selecthost = request.GET['selecthost']
    selectip = request.GET['selectip']
    if selectGroup == "":
        selectGroup = "none"
    if selectGroup != "none" and selecthost != "none" and selectip != "none":
        objs = Basic_Info.objects.filter(ip_addr=selectip)
    else:
        objs = Basic_Info.objects.all()
    info_all = []
    for obj in objs:
        dict = {}
        dict['group_name'] = obj.group_name
        dict['host'] = obj.host
        dict['name'] = obj.host_name
        if obj.status == 0:
            status = "已启用"
        elif obj.status == 1:
            status = "已停用"
        else:
            status = "未知"
        dict['status'] = status
        dict['hostid'] = obj.host_id
        dict['cpu_num'] = obj.cpu_num
        dict['memory_size'] = obj.memory_size
        dict['disk_size'] = obj.disk_size
        dict['ip'] = obj.ip_addr
        utilizationObjs = Utilization.objects.filter(host_id_id=obj.host_id)
        cpu_value_max = 0
        mem_value_max = 0
        disk_use_max = 0
        if utilizationObjs:
            pass
        else:
            dict['cpu_value_min'] = ""
            dict['cpu_value_avg'] = ""
            dict['cpu_value_max'] = 0
            dict['mem_value_min'] = ""
            dict['mem_value_avg'] = ""
            dict['mem_value_max'] = 0

            dict['disk_used'] = ""
            dict['disk_used_percent'] = ""
            timeArray = time.localtime(int(utilobj.clock))
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            dict['date'] = otherStyleTime
        for utilobj in utilizationObjs:
            dict['cpu_value_min'] = utilobj.cpu_value_min
            dict['cpu_value_avg'] = utilobj.cpu_value_avg
            dict['cpu_value_max'] = utilobj.cpu_value_max
            cpu_value_max = utilobj.cpu_value_max
            dict['mem_value_min'] = utilobj.mem_value_min
            dict['mem_value_avg'] = utilobj.mem_value_avg
            dict['mem_value_max'] = utilobj.mem_value_max
            mem_value_max = utilobj.mem_value_max
            dict['disk_used'] = round(utilobj.disk_used, 2)
            if utilobj.disk_used == 0:
                disk_used_percent = 0
            else:
                disk_used_percent = round((utilobj.disk_used / obj.disk_size) * 100, 2)
            dict['disk_used_percent'] = disk_used_percent
            disk_use_max = disk_used_percent
            timeArray = time.localtime(int(utilobj.clock))
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            dict['date'] = otherStyleTime
        if cpu_value_max < cpu_value and mem_value_max < memory_value:
            info_all.append(dict)
        elif cpu_value == 0 and memory_value == 0:
            info_all.append(dict)
        elif cpu_value_max < cpu_value and memory_value == 0:
            info_all.append(dict)
        elif cpu_value == 0 and mem_value_max < memory_value:
            info_all.append(dict)
    info_all = sorted(info_all, key=lambda x: (int(x['cpu_value_max']), int(x['mem_value_max'])))
    return HttpResponse(json.dumps(info_all, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_group_host(request):
    results = []
    objs = Basic_Info.objects.all()
    for obj in objs:
        dict = {}
        dict['id'] = obj.group_name
        dict['text'] = obj.group_name
        dict['pinyin'] = pinyin.get_pinyin(obj.group_name)
        results.append(dict)
    temp_list = list(set([str(i) for i in results]))
    results = [eval(i) for i in temp_list]
    results = sorted(results, key=lambda x: x['pinyin'][0:1].capitalize())

    return HttpResponse(json.dumps(results, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_host_ip(request):
    hostName = request.GET['hostName']
    results = []
    objs = Basic_Info.objects.filter(host=hostName)
    for obj in objs:
        dict = {}
        dict['id'] = obj.ip_addr
        dict['text'] = obj.ip_addr
        results.append(dict)
    return HttpResponse(json.dumps(results, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_list_host(request):
    selectGroup = request.GET['selectGroup']
    results = []
    objs = Basic_Info.objects.filter(group_name=selectGroup)
    for obj in objs:
        dict = {}
        dict['id'] = obj.host
        dict['text'] = obj.host
        dict['pinyin'] = pinyin.get_pinyin(obj.host)
        results.append(dict)
    results = sorted(results, key=lambda x: x['pinyin'][0:1].capitalize())
    return HttpResponse(json.dumps(results, ensure_ascii=False), content_type="application/json,charset=utf-8")
