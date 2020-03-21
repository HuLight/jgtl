from django.db import models


# Create your models here.

class EquipmentClassification(models.Model):
    host_id = models.IntegerField(default='', verbose_name='主机标识')
    pid = models.IntegerField(default='', verbose_name='父标识')
    subject = models.CharField(max_length=128, default='', verbose_name='设备所属类别')
    equipment = models.CharField(max_length=128, default='', verbose_name='设备名称')
    path = models.CharField(max_length=128, default='', verbose_name='路径')
    is_display = models.BooleanField(default=True, verbose_name='是否展示')
    sort_no = models.IntegerField(default=0, verbose_name='排序')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'tb_equipment_classification'
        verbose_name = '设备分类表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s:%s' % (self.subject, self.equipment)


class HostGroup(models.Model):
    group_id = models.IntegerField(default='', verbose_name='主机组id')
    name = models.CharField(max_length=128, default='', verbose_name='主机组名称')
    host = models.ManyToManyField(EquipmentClassification)

    class Meta:
        db_table = 'tb_host_group'
        verbose_name = '主机群组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MonitorItem(models.Model):
    GRAPH_CHOICES = (
        (1, "折线图"),
        (2, "条状图"),
        (3, "饼状图")
    )
    item = models.CharField(max_length=128, default='', verbose_name='监控项中文描述')
    item_key = models.CharField(max_length=128, default='', verbose_name='监控项key值')
    graph_type = models.SmallIntegerField(choices=GRAPH_CHOICES, default=1, verbose_name='显示图表类型')
    sorted_no = models.IntegerField(default=0, verbose_name='排序')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    equipment_id = models.ForeignKey(EquipmentClassification, on_delete=models.CASCADE, verbose_name='设备分类')

    class Meta:
        db_table = 'tb_monitor_item'
        verbose_name = '监控项信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.item
