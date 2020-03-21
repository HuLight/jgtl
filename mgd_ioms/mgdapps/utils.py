# -*- coding: utf-8 -*-
import json
import requests
import time

headers = {"Content-Type": "application/json"}


def user_login(url, username, password):
    """用户登录"""
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": username,
            "password": password
        },
        "id": 1
    }
    # 向zabbix接口发起请求
    return zabbix_api(url, headers, data)


def get_hostlist(token, url, headers):
    # 获取已经配置好的主机,
    # 构造请求体
    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": [
                "hostid",
                "host",
                "name",
                "status"
            ],
            "selectInterfaces": [
                "ip"
            ]
        },
        "id": 1,
        "auth": token
    }
    # 向zabbix接口发起请求,获得响应数据
    return zabbix_api(url, headers, data)


def zabbix_api(url, header, data):
    try:
        # 向zabbixapi发起请求
        request = requests.post(url=url, headers=header, data=json.dumps(data))
        dict = json.loads(request.text)
        request.close()
        return dict['result']
    except Exception as e:
        print("err: %s" % e)


def send_data(host, key, token, url, header):
    # 构建zabbix请求体
    data = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": host['hostid'],
            "search": {
                "key_": key
            },
            "sortfield": "name"
        },
        "auth": token,
        "id": 1
    }
    return zabbix_api(url, header, data)


def request_body(hostid, key, token, url, header):
    # 封装获取监控项方法
    # 构建请求体
    data = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": hostid,
            "search": {
                "key_": key
            },
            "sortfield": "name"
        },
        "auth": token,
        "id": 1
    }
    return zabbix_api(url, header, data)


def get_itemid(key, token, url, header):
    # 获取主机监控项itemid
    host_list = get_hostlist(token, url, header)
    # 创建一个字典存放每台主机某监控项的itemid
    itemid_dict = dict()
    for host in host_list:
        # 调用send_data方法
        item_list = send_data(host, key, token, url, header)
        if len(item_list) == 0:
            continue
        itemid_dict[item_list[0]['hostid']] = item_list[0]['itemid']
    return itemid_dict


def get_trend_list(itemid, token, url, header):
    # 封装获取监控项近期趋势方法
    data = {
        "jsonrpc": "2.0",
        "method": "trend.get",
        "params": {
            "output": [
                "itemid",
                "clock",
                "num",
                "value_min",
                "value_avg",
                "value_max",
            ],
            "itemids": [
                itemid
            ],
            "limit": "1",
        },
        "auth": token,
        "id": 1
    }
    return zabbix_api(url, header, data)


def get_history_data(token, url, itemid, history=0, ):
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
            "time_from": int(time.time() - 1800),
            "time_till": int(time.time()),
        },
        "auth": token,
        "id": 1
    }
    return zabbix_api(url, headers, data)


class PyzabbixAPI():

    def __init__(self,url,user,pwd):
        '''
        认证
        '''
        self.zapi = ZabbixAPI(url)
        self.zapi.login(user, pwd)
        self.prioritytostr = {'0': 'ok', '1': '信息', '2': '警告', '3': '严重'}

    def get_hosts(self):
        #"拉取主机列表"
        host_list = self.zapi.host.get(output=["hostid", "host"], selectInterfaces=["ip"])
        host_list = [{'hostid':host['hostid'],'host':host['host'],'ip':host['interfaces'][0]['ip']} for host in host_list]
        # print(host_list)
        return host_list

    def get_ip(self,hostid):
        #根据hostid获取ip
        ipaddr = self.zapi.host.get(hostids=hostid, output=["hostid"], selectInterfaces=["ip"])[0]['interfaces'][0]['ip']
        return ipaddr

    def get_items(self,hostid=""):
        """
        获取监控项
        :param hostid:  可选  不传参默认为获取所有监控项
        :return:
        """

        if hostid:
            item_list = self.zapi.item.get(output=["itemid", "hostid", "name"], hostids=[hostid])
        else:
            item_list = self.zapi.item.get(output=["itemid", "name"])
        # print(len(item_list))
        return item_list

    def get_triggers(self,status=0, unack=0):
        """
        获取触发器
        :param status: 默认为0，即返回所有触发器，为1，返回正在告警的触发器。
        :param unack:默认为0，即返回所有，1，返回未处理的。
        :return: 返回主机，ip，
        """
        if status:
            triggers = self.zapi.trigger.get(
                    only_true=1,
                    skipDependent=1,
                    monitored=1,
                    active=1,
                    output="extend",
                    expandDescription=1,
                    selectHosts=['host'],
                )
        else:
            triggers = self.zapi.trigger.get(
                    # only_true=1,
                    skipDependent=1,
                    monitored=1,
                    active=1,
                    output="extend",
                    expandDescription=1,
                    selectHosts=['host'],
                )
        if unack:
            triggers = self.zapi.trigger.get(
                only_true=1,
                skipDependent=1,
                monitored=1,
                active=1,
                output='extend',
                expandDescription=1,
                selectHosts=['host'],
                withLastEventUnacknowledged=1,
            )

        return triggers
