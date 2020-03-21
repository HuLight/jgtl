import json
import random
import re
import time

import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from mgd_ioms.settings import ZABBIX_USERNAME, ZABBIX_PASSWORD, ZABBIX_API_URL, zabbix_header
from mgdapps.utils import zabbix_api, send_data, request_body


def get_index(request):
    return render(request, "../frontend/pc/X-admin/index.html")


def get_admin_list(request):
    return render(request, "../frontend/pc/X-admin/admin-list.html")


def get_admin_role(request):
    return render(request, "../frontend/pc/X-admin/admin-role.html")


def get_admin_cate(request):
    return render(request, "../frontend/pc/X-admin/admin-cate.html")


def get_admin_rule(request):
    return render(request, "../frontend/pc/X-admin/admin-rule.html")


def detailspage(request):
    """
    详情页面主页
    :param request:
    :return:
    """
    return render(request, '../frontend/pc/detailspage.html')


def network_detailspage(request):
    """
    网络设备监控详情页
    """
    return render(request, '../frontend/pc/network_detailspage.html')


def information(request):
    """
    主机监控详情页
    """
    return render(request, '../frontend/pc/information.html')


def get_template_page(request):
    """动态生成模板"""
    return render(request, '../frontend/pc/template_page.html')


def getGroupid(login_obj):
    """
    获取组信息
    :return:
    """
    group = {}
    data = {"jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": ["groupid", "name"]
            },
            "auth": login_obj['auth_code'],
            "id": 0
            }

    request_obj = requests.post(url=login_obj['zabbix_url'], headers=login_obj['zabbix_header'],
                                data=json.dumps(data))
    dict = json.loads(request_obj.text)
    for i in dict['result']:
        groupid = i['groupid']
        name = i['name']
        group[name] = groupid
    return group


def get_information_bar(request):
    type = request.GET['type']
    login_obj = login_zabbix()  # 登录zabbix
    group = getGroupid(login_obj)
    host = getHost(login_obj, group, type)
    return HttpResponse(json.dumps(host, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_detailspage_info(request):
    """
    获取详细页所有主机信息
    :param request:
    :return:
    """
    hostid = request.GET['hostid']
    interval = float(request.GET['time']) * 3600
    login_obj = login_zabbix()  # 登录zabbix
    host_info = get_host_info(login_obj, hostid)  # 获取主机信息
    cpu_info = get_cpu(login_obj, hostid, interval)  # 获取CPU
    rw_rate = get_rw_rate(login_obj, hostid, interval)  # 获取磁盘读写速率
    memory_utilization = get_memory_utilization(login_obj, hostid, interval)  # 内存使用率
    net_traffic = get_net_traffic(login_obj, hostid, interval)  # 网卡流量
    warned_message = get_warned_message(login_obj, hostid)  # 告警信息
    disk_utilization = get_disk_utilization(login_obj, hostid)
    swap_in_out_info = swap_in_out(login_obj, hostid)  # 内存交换
    return_dict = dict()
    return_dict['host_info'] = host_info
    return_dict['cpu_info'] = cpu_info
    return_dict['rw_rate'] = rw_rate
    return_dict['memory_utilization'] = memory_utilization
    return_dict['net_traffic'] = net_traffic
    return_dict['warned_message'] = warned_message
    return_dict['disk_utilization'] = disk_utilization
    return_dict['swap_in_out_info'] = swap_in_out_info
    return HttpResponse(json.dumps(return_dict, ensure_ascii=False), content_type="application/json,charset=utf-8")


def login_zabbix():
    """
    登录zabbix方法
    :return: zabbix_url,zabbix_header,auth_code
    """
    # 用户认证信息
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params":
            {
                "user": ZABBIX_USERNAME,
                "password": ZABBIX_PASSWORD
            },
        "id": 0
    }
    auth_code = zabbix_api(ZABBIX_API_URL, zabbix_header, data)
    login_dict = dict()
    login_dict['zabbix_url'] = ZABBIX_API_URL
    login_dict['zabbix_header'] = zabbix_header
    login_dict['auth_code'] = auth_code
    return login_dict


def getHost(login_obj, group, type):
    """
    获取group中的hosts信息
    :param login_obj:
    :param group:
    :return:
    """
    group_list = []
    for k in group.keys():
        groupid = group[k]
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "name"],
                "selectInterfaces": [
                    "interfaceid",
                    "ip"
                ],
                "groupids": groupid
            },
            "auth": login_obj['auth_code'],
            "id": 1,
        }
        request_obj = requests.post(url=login_obj['zabbix_url'], headers=login_obj['zabbix_header'],
                                    data=json.dumps(data))
        hosts = json.loads(request_obj.text)
        if hosts['result'] and k != 'Discovered hosts':
            dict_group = {}
            dict_group['groupName'] = k
            dict_group['list'] = hosts
            if type == "1":
                if k.find("网络") != -1:
                    group_list.append(dict_group)
            elif type == "2":
                if k.find("网络") == -1:
                    group_list.append(dict_group)
    return group_list


def get_host(login_obj, hostid=''):
    """
    获取主机
    :return:
    """
    host_list = []
    host_obj = []
    hostid = hostid
    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": [
                "hostid",
                "host",
                "name"
            ],
            "selectInterfaces": [
                "ip"
            ]
        },
        "id": 1,
        "auth": login_obj['auth_code']
    }
    request_obj = requests.post(url=login_obj['zabbix_url'], headers=login_obj['zabbix_header'],
                                data=json.dumps(data))
    all_host_obj = json.loads(request_obj.text)['result']
    request_obj.close()
    for obj in all_host_obj:
        if obj['hostid'] == hostid:
            host_obj = obj
    dict = {}
    dict['host_obj'] = host_obj
    dict['all_host_obj'] = all_host_obj
    return dict


def get_host_info(login_obj, hostid):
    """
    获取主机信息
    :return:
    """
    dict = {}
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    key = "system.sw.os"
    monitor_obj = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    # 取出操作系统信息
    os_name = ''
    if monitor_obj:
        os_name = monitor_obj[0]['lastvalue']
        dict['os_name'] = os_name[0:os_name.find("(")]
    else:
        key = "system.uname"
        monitor_obj = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                login_obj['zabbix_header'])
        dict['os_name'] = monitor_obj[0]['lastvalue'][0:7]
    # 构建获取主机运行时间请求体
    key = "system.uptime"
    monitor_obj = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'],
                            login_obj['zabbix_header'])
    lifetime = ''
    if monitor_obj:
        lifetime = str(round(float(monitor_obj[0]['lastvalue']) / 3600 / 24, 2)) + '天'
    dict['uptime'] = lifetime
    dict['host'] = host_obj['host']
    dict['name'] = host_obj['name']
    dict['ip'] = host_obj['interfaces'][0]['ip']
    state = ''
    if monitor_obj:
        if monitor_obj[0]['state'] == '0':
            state = '正常'
        else:
            state = '异常'
    dict['state'] = state
    return dict


def get_history_data(login_obj, itemid, interval, history=0, ):
    # 获取历史数据
    data = {
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "output": "extend",
            "history": history,
            "itemids": itemid,
            "sortfield": "clock",
            "sortorder": "ASC",
            "time_from": int(time.time() - interval),
            "time_till": int(time.time()),
        },
        "auth": login_obj['auth_code'],
        "id": 1
    }
    request_obj = requests.post(url=login_obj['zabbix_url'], headers=login_obj['zabbix_header'],
                                data=json.dumps(data))
    history_list = json.loads(request_obj.text)['result']
    return history_list


def get_cpu(login_obj, hostid, interval):
    """获取cpu使用率"""
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    key = "system.cpu.util[,idle]"
    # 将cpu空闲率取出来
    cpu_obj = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    if cpu_obj:
        itemid = cpu_obj[0]['itemid']  # 获取到监控id
        history_items = get_history_data(login_obj, itemid, interval)
        historical_dict = {}
        cpu_unilization_time = []
        cpu_unilization_value = []
        for index, item in enumerate(history_items):
            # 转换时间戳
            timeArray = time.localtime(int(item['clock']))
            # 跨天  跨月 数据减少4倍
            if interval > 10000:
                if index % 10 == 0:
                    historica_time = time.strftime("%m-%d", timeArray)
                    value = round(100 - float(item['value']), 2)  # 拿到历史值
                    cpu_unilization_time.append(historica_time)
                    cpu_unilization_value.append(value)
            else:
                historica_time = time.strftime("%H:%M", timeArray)
                value = round(100 - float(item['value']), 2)  # 拿到历史值
                cpu_unilization_time.append(historica_time)
                cpu_unilization_value.append(value)
        historical_dict['period_of_time'] = cpu_unilization_time
        historical_dict['historical_value'] = cpu_unilization_value
        return historical_dict
    else:
        key = "system.cpu.util"
        cpu_obj = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
        if len(cpu_obj) == 0:
            return
        itemid = cpu_obj[0]['itemid']
        history_items = get_history_data(login_obj, itemid, interval)
        historical_dict = {}
        cpu_unilization_time = []
        cpu_unilization_value = []
        for index, item in enumerate(history_items):
            # 转换时间戳
            timeArray = time.localtime(int(item['clock']))
            # 跨天  跨月 数据减少4倍
            if interval > 10000:
                if index % 10 == 0:
                    historica_time = time.strftime("%m-%d", timeArray)
                    value = round(float(item['value']), 2)  # 拿到历史值
                    cpu_unilization_time.append(historica_time)
                    cpu_unilization_value.append(value)
            else:
                historica_time = time.strftime("%H:%M", timeArray)
                value = round(float(item['value']), 2)  # 拿到历史值
                cpu_unilization_time.append(historica_time)
                cpu_unilization_value.append(value)
        historical_dict['period_of_time'] = cpu_unilization_time
        historical_dict['historical_value'] = cpu_unilization_value
        return historical_dict


def get_rw_rate(login_obj, hostid, interval):
    """
    获取磁盘读写速率
    :param login_obj: 登录信息
    :param hostid: 主机id
    :param interval: 时间戳
    :return: historical_dict
    """
    # 取出磁盘读速率
    key = "vfs.dev.read.rate[sda]"
    read_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    if read_list:
        itemid = read_list[0]['itemid']  # 获取到监控id
    else:
        return
    history_items = get_history_data(login_obj, itemid, interval)
    historical_dict = {}
    write_rate_time = []
    write_rate_value = []
    read_rate_value = []
    for index, item in enumerate(history_items):
        # 转换时间戳
        timeArray = time.localtime(int(item['clock']))
        # 数据减少一倍
        if interval > 10000:
            if index % 10 == 0:
                historica_time = time.strftime("%m-%d", timeArray)
                value = item['value']  # 拿到历史值
                write_rate_time.append(historica_time)
                read_rate_value.append(value)
        else:
            historica_time = time.strftime("%H:%M", timeArray)
            value = item['value']  # 拿到历史值
            write_rate_time.append(historica_time)
            read_rate_value.append(value)
    historical_dict['write_rate_time'] = write_rate_time
    historical_dict['read_rate_value'] = read_rate_value
    # 取出磁盘写速率,放进字典中
    key = "vfs.dev.write.rate[sda]"
    write_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    itemid = write_list[0]['itemid']  # 获取到监控id
    history_items = get_history_data(login_obj, itemid, interval)
    for index, item in enumerate(history_items):
        # 数据减少一倍
        if interval > 10000 and index % 10 == 0:
            value = item['value']  # 拿到历史值
            write_rate_value.append(value)
        else:
            value = item['value']  # 拿到历史值
            write_rate_value.append(value)
    historical_dict['write_rate_value'] = write_rate_value
    return historical_dict


def get_memory_utilization(login_obj, hostid, interval):
    """
    获取内存使用率
    :param login_obj: 登录信息
    :param hostid: 主机id
    :param interval: 时间戳
    :return: historical_dict
    """
    key = "vm.memory.size[pavailable]"
    # 将内存使用率取出
    memory_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    if memory_list:
        itemid = memory_list[0]['itemid']  # 获取到监控id
        history_items = get_history_data(login_obj, itemid, interval)
        historical_dict = {}
        memory_unilization_time = []
        memory_unilization_value = []
        for index, item in enumerate(history_items):
            # 转换时间戳
            timeArray = time.localtime(int(item['clock']))
            # 数据减少一倍
            if interval > 10000:
                if index % 10 == 0:
                    historica_time = time.strftime("%m-%d", timeArray)
                    value = item['value']  # 拿到历史值
                    memory_unilization_time.append(historica_time)
                    memory_unilization_value.append(value)
            else:
                historica_time = time.strftime("%H:%M", timeArray)
                value = item['value']  # 拿到历史值
                memory_unilization_time.append(historica_time)
                memory_unilization_value.append(value)
        historical_dict['memory_unilization_time'] = memory_unilization_time
        historical_dict['memory_unilization_value'] = memory_unilization_value
        return historical_dict
    else:
        key = "vm.memory.util"
        # 将内存使用率取出
        memory_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                   login_obj['zabbix_header'])
        if len(memory_list) == 0:
            return
        itemid = memory_list[0]['itemid']  # 获取到监控id
        history_items = get_history_data(login_obj, itemid, interval)
        historical_dict = {}
        memory_unilization_time = []
        memory_unilization_value = []
        for index, item in enumerate(history_items):
            # 转换时间戳
            timeArray = time.localtime(int(item['clock']))
            # 数据减少一倍
            if interval > 10000:
                if index % 10 == 0:
                    historica_time = time.strftime("%m-%d", timeArray)
                    value = item['value']  # 拿到历史值
                    memory_unilization_time.append(historica_time)
                    memory_unilization_value.append(value)
            else:
                historica_time = time.strftime("%H:%M", timeArray)
                value = item['value']  # 拿到历史值
                memory_unilization_time.append(historica_time)
                memory_unilization_value.append(value)
        historical_dict['memory_unilization_time'] = memory_unilization_time
        historical_dict['memory_unilization_value'] = memory_unilization_value
        return historical_dict


def get_net_traffic(login_obj, hostid, interval):
    """
    获取出入口流量
    :param login_obj: 登录信息
    :param hostid: 主机id
    :param interval: 时间戳
    :return: historical_dict
    """
    # 构造请求体
    key = "net.if.in"
    net_in_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    itemid = ''
    for i in net_in_list:
        # 流入流量
        if re.match('^net.if.in\["\w+"\]$', i['key_']):
            itemid = i['itemid']
    if itemid == '':
        return
    history_items = get_history_data(login_obj, itemid, interval, 3)
    historical_dict = {}
    received_traffic_time = []
    received_traffic_value = []
    for index, item in enumerate(history_items):
        # 转换时间戳
        timeArray = time.localtime(int(item['clock']))
        # 数据减少一倍
        if interval > 10000:
            if index % 10 == 0:
                historica_time = time.strftime("%m-%d", timeArray)
                value = round(float(item['value']) / 1000, 2)  # 拿到历史值
                received_traffic_time.append(historica_time)
                received_traffic_value.append(value)
        else:
            historica_time = time.strftime("%H:%M", timeArray)
            value = round(float(item['value']) / 1000, 2)  # 拿到历史值
            received_traffic_time.append(historica_time)
            received_traffic_value.append(value)
    historical_dict['received_traffic_time'] = received_traffic_time
    historical_dict['received_traffic_value'] = received_traffic_value
    sent_traffic_time = []
    sent_traffic_value = []
    # 构造流出流量请求体
    key = "net.if.out"
    net_out_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                login_obj['zabbix_header'])
    for i in net_out_list:
        # 流出的流量
        if re.match('^net.if.out\["\w+"\]$', i['key_']):
            itemid = i['itemid']  # 获取到监控id
    history_items = get_history_data(login_obj, itemid, interval, 3)
    for index, item in enumerate(history_items):
        if interval > 10000:
            if index % 10 == 0:
                historica_time = time.strftime("%m-%d", timeArray)
                value = round(float(item['value']) / 1000, 2)  # 拿到历史值
                sent_traffic_time.append(historica_time)
                sent_traffic_value.append(value)
        else:
            historica_time = time.strftime("%H:%M", timeArray)
            value = round(float(item['value']) / 1000, 2)  # 拿到历史值
            sent_traffic_time.append(historica_time)
            sent_traffic_value.append(value)
    historical_dict['sent_traffic_time'] = sent_traffic_time
    historical_dict['sent_traffic_value'] = sent_traffic_value
    return historical_dict


def get_warned_message(login_obj, hostid):
    """获取告警信息"""
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    # 构建获取触发器信息请求体
    data = {
        "jsonrpc": "2.0",
        "method": "trigger.get",
        "params": {
            "output": "extend",
            "filter": {
                "value": 1
            },
            "sortfield": "priority",
            "sortorder": "DESC",
            "min_severity": 2,
            "skipDependent": 1,
            "monitored": 1,
            "active": 1,
            "expandDescription": 1,
            "selectHosts": ['host'],
            "selectGroups": ['name'],
            "only_true": 1
        },
        "auth": login_obj['auth_code'],
        "id": 1
    }
    trigger_list = zabbix_api(login_obj['zabbix_url'], login_obj['zabbix_header'], data)
    # 创建一个空列表存储所有触发器告警信息
    warned_list = list()
    for i in trigger_list:
        trigger_dict = dict()
        # 告警信息
        trigger_dict['description'] = i['description']
        # 告警的主机名字
        trigger_dict['name'] = i['hosts'][0]['host']
        # 判断告警程度
        if i['priority'] == '2':
            trigger_dict['priority'] = '警告'
        elif i['priority'] == '3':
            trigger_dict['priority'] = '一般严重'
        elif i['priority'] == '4':
            trigger_dict['priority'] = '严重'
        elif i['priority'] == '5':
            trigger_dict['priority'] = '灾难'
        # 触发器ID
        trigger_dict['triggerid'] = i['triggerid']
        # 触发时间
        # 获取时间戳
        timestamp = i['lastchange']
        time_array = time.localtime(int(timestamp))
        other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        trigger_dict['trigger_time'] = other_style_time
        if i['status'] == '0':
            trigger_dict['status'] = '问题'
        # 将构建触发器告警信息存入warned_list中
        warned_list.append(trigger_dict)
    # 只获取当前主机告警信息
    current_host_warned = []
    for item in warned_list:
        if item['name'] == host_obj['host']:
            current_host_warned.append(item)
    if not current_host_warned:
        trigger_dict = dict()
        trigger_dict['trigger_time'] = '暂无告警信息'
        trigger_dict['priority'] = ''
        trigger_dict['status'] = ''
        trigger_dict['status'] = ''
        trigger_dict['name'] = ''
        trigger_dict['description'] = ''
        current_host_warned.append(trigger_dict)
    return current_host_warned


def get_disk_utilization(login_obj, hostid):
    """
    获取磁盘使用率
    :param login_obj: 登录信息
    :param hostid: 主机id
    :return: usage_dict
    """
    key = "vfs.fs.size[/boot,pused]"
    boot_disk_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                  login_obj['zabbix_header'])
    if len(boot_disk_list) == 0:
        # 获取黄羊机器的C盘使用率
        key = "vfs.fs.size[C:,pused]"
        disk_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                 login_obj['zabbix_header'])
        c_disk_utilization = disk_list[0]['lastvalue']
        # 获取黄羊机器的D盘使用率
        key = "vfs.fs.size[D:,pused]"
        disk_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                 login_obj['zabbix_header'])
        d_disk_utilization = disk_list[0]['lastvalue']
        hard_disk_mount_point = ["C", "D"]
        disk_usage = [c_disk_utilization, d_disk_utilization]
        usage_dict = dict()
        usage_dict['hard_disk_mount_point'] = hard_disk_mount_point
        usage_dict['disk_usage'] = disk_usage
        return usage_dict
    else:
        # /boot磁盘使用率
        boot_utilization = boot_disk_list[0]['lastvalue']
        key = "vfs.fs.size[/,pused]"
        root_disk_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                      login_obj['zabbix_header'])
        # 根目录使用率
        root_utilization = root_disk_list[0]['lastvalue']
        hard_disk_mount_point = ["/", "/boot"]
        disk_usage = [root_utilization, boot_utilization]
        usage_dict = dict()
        usage_dict['hard_disk_mount_point'] = hard_disk_mount_point
        usage_dict['disk_usage'] = disk_usage
        return usage_dict


def swap_in_out(login_obj, hostid):
    """
    获取内存交换
    :param login_obj: 登录信息
    :param hostid: 主机id
    :return: swap_dict
    """
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    key = "system.swap.size[,total]"
    data = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    # 创建一个空字典存放内存交换值
    swap_dict = dict()
    if data:
        swap_size = str(round(int(data[0]['lastvalue']) / 1024 ** 3, 2))
        swap_dict['swap_size'] = swap_size
        return swap_dict
    else:
        return


def get_network_equipment_info(request):
    """
        获取网络设备信息
        :param request:
        :return:
    """
    hostid = request.GET['hostid']
    login_obj = login_zabbix()  # 登录zabbix
    network_host_info = get_network_host_info(login_obj, hostid)
    physical_status = get_physical_status(login_obj, hostid)
    warned_message = get_warned_message(login_obj, hostid)  # 告警信息
    net_traffic_top5 = get_net_traffic_top5(login_obj, hostid)  # 获取前TOP5流量端口
    port_state = get_port_state(login_obj, hostid)
    net_traffic = get_net_traffic(login_obj, hostid, 100)  # 网卡流量
    err_packet = get_err_packet(login_obj, hostid)  # 错包
    port_percent = get_port_percent(hostid, login_obj)  # 端口流量百分比前10名
    port_value_top10 = sum_port_top10(hostid, login_obj)  # 端口流量大小前10名
    dict = {}
    dict['network_host_info'] = network_host_info
    dict['physical_status'] = physical_status
    dict['warned_message'] = warned_message
    dict['net_traffic_top5'] = net_traffic_top5
    dict['port_state'] = port_state
    dict['net_traffic'] = net_traffic
    dict['err_packet'] = err_packet
    dict['port_percent'] = port_percent
    dict['port_value_top10'] = port_value_top10
    return HttpResponse(json.dumps(dict, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_network_host_info(login_obj, hostid):
    """获取监控的网络设备信息"""
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    # 搜索键值key
    key = "system.name"
    data = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    # 将系统名称取出存入switch_list中
    dict = {}
    if data:
        dict['system_name'] = data[0]['lastvalue']
        dict['name'] = host_obj['name']
        dict['ip'] = host_obj['interfaces'][0]['ip']
        if data[0]['state'] == '0':
            state = "正常"
        else:
            state = "异常"
        dict['state'] = state
        # 搜索键值为运行时间
        key = "system.uptime"
        # 构建请求体,向zabbix发起请求
        data = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
        uptime = str(round(float(data[0]['lastvalue']) / 3600 / 24, 2)) + "天"
        dict['uptime'] = uptime
    return dict


def get_physical_status(login_obj, hostid):
    """获取设备物理状态"""
    # 获取设备列表
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    dict = {}
    # cpu使用率
    # 搜索键值cpu_usage[212]
    key = "cpu_usage[212]"
    # 构造请求体,向zabbix发起请求,得到cpu使用率
    data = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    if data:
        cpu_usage = data[0]['lastvalue']
        # 内存使用率
        # 搜索键值key:mem_usage[212]
        key = "mem_usage[212]"
        # 构建请求体,向zabbix发起请求
        data = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
        memory_usage = data[0]['lastvalue']
        disk_usage = ""
        dict['usage'] = [disk_usage, memory_usage, cpu_usage]
        # 获取设备的风扇状态和电源状态
        # 搜索键值key:风扇:sensor.fan.status
        key = "sensor.fan.status"
        # 构建请求体,向zabbix发起请求
        data = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
        if len(data) == 0:
            return dict
        # 遍历去取出风扇状态
        for index, element in enumerate(data, start=1):
            # 判断风扇状态
            if element['lastvalue'] == '1':
                element['lastvalue'] = "正常"
            elif element['lastvalue'] == '2':
                element['lastvalue'] = "警告"
            elif element['lastvalue'] == '3':
                element['lastvalue'] = "严重警告"
            elif element['lastvalue'] == '4':
                element['lastvalue'] = "关闭"
            elif element['lastvalue'] == '5':
                element['lastvalue'] = "不存在"
            elif element['lastvalue'] == '6':
                element['lastvalue'] = "无功能"
            dict['fan' + str(index)] = element['lastvalue']
        # 电源状态
        # 搜索键值key:sensor.psu.status
        key = "sensor.psu.status"
        # 构建请求体,向zabbix发起请求
        data = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
        dict['power'] = data[0]['lastvalue']
        return dict
    else:
        return {}


def get_port_state(login_obj, hostid):
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    key = "net.if.status"
    datas = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    # 获取监控的端口名和状态
    dict = {}
    port_state_list = []
    normal_value = 0
    abnormal_value = 0

    for data in datas:
        # dict[data['name'][data['name'].find("E"):data['name'].find(":")]] = data['lastvalue']
        if data['lastvalue'] == '1':
            state = 'up'
            normal_value += 1
        else:
            state = 'down'
            abnormal_value += 1
        dict = {}
        dict['name'] = data['name'][:data['name'].find(":")].replace(" ", "")
        dict['state'] = state
        port_state_list.append(dict)
    dict = {}
    dict['normal_value'] = normal_value
    dict['abnormal_value'] = abnormal_value
    dict['port_state_list'] = port_state_list
    print("dict==", dict)

    return dict


def get_net_traffic_top5(login_obj, hostid):
    """获取端口流量前五名"""
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    # 创建一个空字典
    net_in_dict = {}
    # 搜索key值:port.inbytes
    key = "port.inbytes"
    # 构造请求体,向zabbix发起请求,获取流入流量
    data = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    # 将流出流量取出放入net_in_dict中
    try:
        for index, element in enumerate(data, start=0):
            # 用正则匹配出端口名字构造出net_out_dict键值
            net_in_dict[re.findall('\[\w+\/\d+\/\d+\]$', element['key_'])[0]] = round(float(element['lastvalue']), 2)
        # 创建一个空字典
        net_out_dict = {}
        # 搜索键值key:port.outbytes
        key = "port.outbytes"
        # 构造请求体,向zabbix发起请求,获取流出流量
        data = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
        # 将流出流量取出放入net_out_dict中
        for index, element in enumerate(data, start=1):
            # 用正则匹配出端口名字构造出net_out_dict键值
            net_out_dict[re.findall('\[\w+\/\d+\/\d+\]$', element['key_'])[0]] = round(float(element['lastvalue']), 2)
    except Exception as e:
        return {}
    # for index, element in enumerate(data, start=1):
    #     # 用正则匹配出端口名字构造出net_out_dict键值
    #     net_out_dict[element['key_']] = round(float(element['lastvalue']),2)
    # 创建一个空字典来存放流入和流出流量之和
    sum_dict = {}
    # 遍历net_in_dict的key
    for key in net_in_dict:
        # 如果这个key在net_out_dict,即两者value值相加
        if key in net_out_dict:
            sum_dict[key] = net_in_dict[key] + net_out_dict[key]
    # 按照字典的value值排序,返回一个列表,key和value值转换成字典
    net_list = sorted(sum_dict.items(), key=lambda item: item[1])
    # 取出排序大小前五位
    net_list = net_list[:-11:-1]
    ranking_top5_value = []
    ranking_top5_name = []
    # echarts 从最后一位开始加载,所以此处倒序排列
    for item in reversed(net_list):
        ranking_top5_name.append(item[0][item[0].find("E"):-1])
        ranking_top5_value.append(round(float(item[1] / 1000), 2))
    dict = {}
    dict['ranking_top5_name'] = ranking_top5_name
    dict['ranking_top5_value'] = ranking_top5_value
    return dict


def get_err_packet(login_obj, hostid):
    """
    获取错包数
    :param login_obj:
    :param hostid:
    :return:
    """
    # 创建一个字典来存放进出流量错误包之和
    err_dict = {}
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    # 创建一个字典来存放进流量错误包
    flow_in_dict = {}
    # 获取网络端口进流量错包数
    key = 'port.inerr'
    port_in_list = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    if port_in_list:
        for port in port_in_list:
            # 正则匹配端口名称
            if re.match('^port.(\w)*\[(.*)\]$', port['key_']):
                ret = re.match('^port.(\w)*\[(.*)\]$', port['key_'])
                flow_in_dict[ret.group(2)] = port['lastvalue']
        # 创建一个字典来存放出流量错误包
        flow_out_dict = {}
        key = 'port.outerr'
        port_out_list = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                  login_obj['zabbix_header'])
        for port in port_out_list:
            if re.match('^port.(\w)*\[(.*)\]$', port['key_']):
                ret = re.match('^port.(\w)*\[(.*)\]$', port['key_'])
                flow_out_dict[ret.group(2)] = port['lastvalue']
        # 将每个端口的进流量错误包和出流量错误包相加
        for i in flow_in_dict:
            err_dict[i] = str(round(float(flow_in_dict[i]) + float(flow_out_dict[i]), 2))
        # 按照字典的value值排序,返回一个列表,key和value值转换成字典
        sorted_list = sorted(err_dict.items(), key=lambda item: item[1])[:-11:-1]
        name = []
        value = []
        for item in reversed(sorted_list):
            if float(item[1]) > 0:
                name.append(item[0][item[0].find("E"):-1])
                value.append(item[1])
        dict = {}
        dict['name'] = name
        dict['value'] = value
        return dict
    else:
        return


def get_discard_packet(hostid, login_obj):
    """
    获取端口丢包数
    :param hostid: 主机id
    :param login_obj: 登录信息
    :return: sorted_list
    """
    # 创建字典存放端口进流量丢包数
    discard_in_dict = dict()
    key = "net.if.in.discards"
    discard_in_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                   login_obj['zabbix_header'])
    for i in discard_in_list:
        ret = re.match(r"([a-zA-Z0-9/]+\s[a-zA-Z]+\d/\d/\d+)", i['name'])
        if ret:
            # 用正则匹配将端口名称取出
            index = ret.group().index(' ') + 1
            port_key = ret.group()[index:]
            discard_in_dict[port_key] = i['lastvalue']
    # 创建字典存放端口出流量丢包数
    discard_out_dict = dict()
    key = "net.if.out.discards"
    discard_out_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                    login_obj['zabbix_header'])
    for i in discard_out_list:
        ret = re.match(r"([a-zA-Z0-9/]+\s[a-zA-Z]+\d/\d/\d+)", i['name'])
        if ret:
            # 用正则匹配将端口名称取出
            index = ret.group().index(' ') + 1
            port_key = ret.group()[index:]
            discard_out_dict[port_key] = i['lastvalue']
    # 创建字典存放丢包数总和
    discard_sum_dict = dict()
    for i in discard_in_dict:
        discard_sum_dict[i] = discard_in_list[i] + discard_out_dict[i]
    # 按照字典的value值排序,返回一个列表,key和value值转换成字典,并取出top10
    sorted_list = sorted(discard_sum_dict.items(), key=lambda item: item[1])[:-11:-1]
    return sorted_list


def get_port_bytes(hostid, login_obj, key):
    """
    传入不同的键值获取端口不同类型的流量
    :param hostid: 主机id
    :param login_obj: 登录信息
    :param key:流量类型
    :return:设备端口流量
    """
    # 创建一个字典来存放进出流量
    flow_dict = dict()
    # host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    port_in_list = request_body(hostid, key, login_obj['auth_code'], login_obj['zabbix_url'],
                                login_obj['zabbix_header'])
    for port in port_in_list:
        # 正则匹配端口名称
        if re.match('^port.(\w)*\[(.*)\]$', port['key_']):
            ret = re.match('^port.(\w)*\[(.*)\]$', port['key_'])
            flow_dict[ret.group(2)] = port['lastvalue']
    return flow_dict


def get_port_sum(hostid, login_obj):
    """
    获取进出流量大小
    :param hostid: 主机id
    :param login_obj: 登录信息
    :return: sum_dict
    """
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    # 获取进流量
    key = 'port.inbytes'
    port_in_dict = get_port_bytes(host_obj, login_obj, key)
    # 获取出流量
    key = 'port.outbytes'
    port_out_dict = get_port_bytes(host_obj, login_obj, key)
    # 创建一个字典存放进出流量之和
    sum_dict = dict()
    for i in port_in_dict:
        sum_dict[i] = float(port_in_dict[i]) + float(port_out_dict[i])
    return sum_dict


def sum_port_top10(hostid, login_obj):
    """
    获取端口流量大小top10
    :param hostid: 主机id
    :param login_obj: 登录信息
    :return: sorted_list
    """
    sum_dict = get_port_sum(hostid, login_obj)
    # 按照字典的value值排序,返回一个列表,key和value值转换成字典
    sorted_list = sorted(sum_dict.items(), key=lambda item: item[1])[:-11:-1]
    name = []
    value = []
    for item in reversed(sorted_list):
        if float(item[1]) > 0:
            name.append(item[0][item[0].find("E"):-1])
            value.append(item[1])
    dict = {}
    dict['name'] = name
    dict['value'] = value
    return dict


def get_port_percent(hostid, login_obj):
    """
    # 获取端口流量百分比top10
    :param hostid: 主机id
    :param login_obj: 登录信息
    :return: sorted_list
    """
    # 调用get_port_sum方法获取到每个端口流量大小
    sum_dict = get_port_sum(hostid, login_obj)
    # 创建一个字典存放每个端口流量百分比
    port_percent = {}
    for i in sum_dict:
        # 因为每个端口GigabitEthernet：千兆端口,即除以10**9,获得流量百分比
        port_percent[i] = round(float(sum_dict[i]) / 10 ** 9, 5) * 100
    # 按照字典的value值排序,返回一个列表,key和value值转换成字典
    sorted_list = sorted(port_percent.items(), key=lambda item: item[1])[:-11:-1]
    name = []
    value = []
    for item in reversed(sorted_list):
        if float(item[1]) > 0:
            name.append(item[0][item[0].find("E"):-1])
            value.append(item[1])
    dict = {}
    dict['name'] = name
    dict['value'] = value
    return dict


def get_port(login_obj, hostid, key):
    """
    此方法为工具方法，用来被获取端口相关信息时调用
    :param login_obj: 登录信息
    :param hostid: 主机id
    :param key: 所取监控项键值
    :return: port_dict
    """
    host_obj = get_host(login_obj, hostid)['host_obj']  # 获取主机
    # 获取端口状态
    # 创建一个字典存放端口相关信息
    port_dict = dict()
    data = send_data(host_obj, key, login_obj['auth_code'], login_obj['zabbix_url'], login_obj['zabbix_header'])
    for i in data:
        ret = re.match(r"([a-zA-Z0-9/]+\s[a-zA-Z]+\d/\d/\d+)", i['name'])
        if ret:
            # 将端口名称中空格去除掉
            index = ret.group().index(' ') + 1
            port_key = ret.group()[index:]
            port_dict[port_key] = i['lastvalue']
    return port_dict


def get_port_info(request):
    """
    获取端口属性及指标信息
    :param login_obj: 登录信息
    :param hostid: 主机id
    :param port: 端口号
    :return:
    """
    hostid = request.GET['hostid']
    portName = request.GET['portName']
    portName = portName[9:]
    login_obj = login_zabbix()  # 登录zabbix
    # 获取端口状态
    key = "net.if.status"
    port_status = get_port(login_obj, hostid, key)
    # 获取端口类型
    key = "net.if.type"
    port_type = get_port(login_obj, hostid, key)
    # 获取端口速率
    key = "net.if.speed"
    port_speed = get_port(login_obj, hostid, key)
    # 获取端口流量大小
    sum_dict = get_port_sum(hostid, login_obj)
    # 创建一个字典存放所有端口相关信息
    port_dict = dict()
    for i in port_status:
        # 创建一个字典存放端口相关信息
        port_info = dict()
        if port_status[i] == '1':
            port_info['status'] = 'up'
        else:
            port_info['status'] = 'down'
        port_info['type'] = port_type[i]
        port_info['speed'] = port_speed[i]
        port_info['traffic'] = round(sum_dict[i], 2)
        port_info['mac_addr'] = ''
        port_dict[i] = port_info
    return HttpResponse(json.dumps(port_dict[portName], ensure_ascii=False),
                        content_type="application/json,charset=utf-8")


def get_template_data(request):
    page = request.GET['page']
    print("page==",page)
    dict = {}
    results = []
    for i in range(1, 11):
        temp = {}
        if i % 2 == 0:
            temp['type'] = "line"
        else:
            temp['type'] = "bar"
        temp['time'] = ['2:10', '2:11', '2:12', '2:13', '2:14', '2:15', '2:16', '2:17', '2:18', '2:19']
        nums = []
        count = 0
        while True:
            num = random.randint(10, 70)
            nums.append(num)
            count = count + 1
            if count == 10:
                break
        temp['data'] = nums
        results.append(temp)
    start = (int(page) - 1) * 4
    end = (int(page) * 4)
    dict['total'] = len(results)
    results = results[start:end]
    print("results", results)

    dict['results'] = results
    return HttpResponse(json.dumps(dict, ensure_ascii=False), content_type="application/json,charset=utf-8")
