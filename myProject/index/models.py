from django.db import models

class ShareData(models.Model):
    date = models.DateField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    price_change = models.FloatField(blank=True, null=True)
    p_change = models.FloatField(blank=True, null=True)
    ma5 = models.FloatField(blank=True, null=True)
    ma10 = models.FloatField(blank=True, null=True)
    ma20 = models.FloatField(blank=True, null=True)
    sort = models.ForeignKey('ShareSort', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'share_data'


class ShareSort(models.Model):
    share_name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'share_sort'