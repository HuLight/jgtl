from configparser import ConfigParser
import json
import requests
import os
from mgd_ioms.settings import BASE_DIR
#   获取配置信息
conf = ConfigParser()
conf.read(os.path.join(BASE_DIR,"config/zabbix.conf"),encoding='utf-8')
url = conf.get("zabbix", "api_url")
username = conf.get("zabbix", "username")
password = conf.get("zabbix", "password")
headers = {"Content-Type": "application/json-rpc"}

def get_auth():
    """获取身份令牌"""
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": username,
            "password": password,
        },
        "id": 0,
    }
    return get_response(data)



def get_response(data):
    """获取response对象,返回字典数据"""

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
    except Exception as e:
        print("get_response")
        return
    return json.loads(response.text).get('result')