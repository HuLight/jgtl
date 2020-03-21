from django.db import models


class Basic_Info(models.Model):
    STATUS_CHOICES = (
        (0, "已启用"),
        (1, "已停用"),
    )
    clock = models.IntegerField(default=0, verbose_name='时间戳')
    groupid = models.BigIntegerField(default=0, verbose_name='主机组id')
    group_name = models.CharField(max_length=128, default='', verbose_name='主机组名称')
    host_id = models.BigIntegerField(primary_key=True, verbose_name='主机id')
    host = models.CharField(max_length=128, default='', verbose_name='主机')
    host_name = models.CharField(max_length=128, default='', verbose_name='主机名称')
    ip_addr = models.CharField(max_length=128, default='', verbose_name='ip地址')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name='主机状态')
    cpu_num = models.IntegerField(default=0, verbose_name='cpu个数')
    memory_size = models.IntegerField(default=0, verbose_name='内存大小')
    disk_size = models.IntegerField(default=0, verbose_name='磁盘大小')

    class Meta:
        db_table = 'tb_basic_info'
        verbose_name = "主机基本信息"
        unique_together = (("clock", "host_id"),)
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.host_name


class Utilization(models.Model):
    clock = models.IntegerField(default=0, verbose_name='时间戳')
    host_id = models.ForeignKey(Basic_Info, default=0, verbose_name='主机id', on_delete=models.CASCADE)
    cpu_clock = models.IntegerField(default=0, verbose_name='cpu时间戳')
    cpu_value_min = models.FloatField(max_length=16, default=0, verbose_name='cpu谷值')
    cpu_value_max = models.FloatField(max_length=16, default=0, verbose_name='cpu峰值')
    cpu_value_avg = models.FloatField(max_length=16, default=0, verbose_name='cpu均值')
    mem_clock = models.IntegerField(default=0, verbose_name='内存时间戳')
    mem_value_min = models.FloatField(max_length=16, default=0, verbose_name='内存谷值')
    mem_value_avg = models.FloatField(max_length=16, default=0, verbose_name='内存均值')
    mem_value_max = models.FloatField(max_length=16, default=0, verbose_name='内存峰值')
    disk_clock = models.IntegerField(default=0, verbose_name='磁盘时间戳')
    disk_used = models.FloatField(max_length=16, default=0, verbose_name='磁盘使用率')

    class Meta:
        db_table = 'tb_utilization'
        verbose_name = '监控项使用率'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.host_id