import os
import sys
import  django
from datetime import datetime
from configparser import ConfigParser

os.environ['DJANGO_SETTINGS_MODULE'] = 'mgd_ioms.settings'
django.setup()

from mgdapps.utils import PyzabbixAPI
from mgdapps import models


cp = ConfigParser()
cp.read('../../config/zabbix.conf')
ZABBIX_NAME = cp.get("zabbix_test1","name")
ZABBIX_API_URL = cp.get("zabbix_test1", "api_url")
ZABBIX_USERNAME = cp.get("zabbix_test1", "username")
ZABBIX_PASSWORD = cp.get("zabbix_test1", "password")

# print(ZABBIX_API_URL)
#

#获取日报数据入库
def gen_alarm_daily():
    zapi = PyzabbixAPI(ZABBIX_API_URL, ZABBIX_USERNAME, ZABBIX_PASSWORD)
    date = datetime.now().date()
    name = u'{}日报'.format(ZABBIX_NAME)
    exec_time = datetime.now()
    hosts_count = len(zapi.get_hosts())
    items_count =len(zapi.get_items())
    triggers_count = len(zapi.get_triggers())
    problems = zapi.get_triggers(status=1)
    problems_count = len(problems)

    mdobj = models.MonitorDaily.objects.create(
        date = date,
        name = name,
        exec_time = exec_time,
        hosts_count = hosts_count,
        items_count = items_count,
        triggers_count = triggers_count,
        problems_count =problems_count
    )
    print(mdobj)

    unack_problems = zapi.get_triggers(status=1,unack=1)

    unack_trigger_ids = [t['triggerid'] for t in unack_problems]
    for t in problems:
        t['unacknowledged'] = True if t['triggerid'] in unack_trigger_ids else False

    [ models.ProblemDetails(p['hosts'][0]['host'],


                            )
      for p in problems]

gen_alarm_daily()