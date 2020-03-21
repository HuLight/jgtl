from django.db import models

# 监控日报
class MonitorDaily(models.Model):
    date = models.DateTimeField(u'日期',auto_now=True)
    name = models.CharField(u'任务名称', max_length=100)
    exec_time = models.DateTimeField(u'时间', auto_now=True)
    hosts_count = models.IntegerField(u'监控主机数')
    items_count = models.IntegerField(u'监控指标数')
    triggers_count = models.IntegerField(u'触发器数')
    problems_count = models.IntegerField(u'告警数')
    # problem_details = models.ForeignKey('ProblemDetails', verbose_name=u'告警详情', on_delete=models.CASCADE)

    # file = models.FileField('pdf_report',upload_to='pdf_report')

    class Meta:
        db_table = 'tb_monitor_daily'
        verbose_name = "zabbix监控日报表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '< %s:%s >' % (self.date, self.name)


# 告警详情表
class ProblemDetails(models.Model):
    PRIORITY_CHOICES = (
        ("0", u"ok"),
        ("1", u"信息"),
        ("2", u"警告"),
        ("3", u"严重"),
    )
    UNACK_CHOICES = (
        ("0",u'已处理'),
        ("1",u'未处理')
    )
    hostname = models.CharField(u'异常主机名称',max_length=100,null=True)
    ip = models.CharField(u'主机ip',max_length=128,default="")
    time = models.DateTimeField(u'告警时间',auto_now=True)
    priority = models.IntegerField(u'告警优先级',choices=PRIORITY_CHOICES,default=0)
    descript = models.TextField(u'告警详情',null=True)
    unack = models.IntegerField(u'是否未处理',choices=UNACK_CHOICES,default=0)
    monitor_daily = models.ForeignKey(MonitorDaily,verbose_name=u'所属日报',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'tb_problem_details'
        verbose_name = "告警详情表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "< %s:%s >" % (self.hostname, self.descript)
