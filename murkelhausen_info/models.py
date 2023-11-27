from django.db import models


class MurkelhausenStates(models.Model):
    id = models.BigIntegerField(primary_key=True)
    tstamp = models.DateTimeField(blank=True, null=True)
    message_tstamp = models.DateTimeField(blank=True, null=True)
    hostname = models.TextField(blank=True, null=True)
    uptime = models.BigIntegerField(blank=True, null=True)
    memory_total = models.BigIntegerField(blank=True, null=True)
    memory_available = models.BigIntegerField(blank=True, null=True)
    memory_used = models.BigIntegerField(blank=True, null=True)
    memory_used_percent = models.FloatField(blank=True, null=True)
    memory_free = models.BigIntegerField(blank=True, null=True)
    cpu_cores = models.BigIntegerField(blank=True, null=True)
    cpu_logical = models.BigIntegerField(blank=True, null=True)
    cpu_usage_avg = models.FloatField(blank=True, null=True)
    root_disk_total = models.BigIntegerField(blank=True, null=True)
    root_disk_free = models.BigIntegerField(blank=True, null=True)
    root_disk_used = models.BigIntegerField(blank=True, null=True)
    root_disk_used_percent = models.FloatField(blank=True, null=True)
    load01 = models.FloatField(blank=True, null=True)
    load05 = models.FloatField(blank=True, null=True)
    load15 = models.FloatField(blank=True, null=True)
    network_bytes_sent = models.BigIntegerField(blank=True, null=True)
    network_bytes_recv = models.BigIntegerField(blank=True, null=True)
    process_count = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "murkelhausen_states"


class PowerData(models.Model):
    id = models.BigIntegerField(primary_key=True)
    tstamp = models.DateTimeField(blank=True, null=True)
    message_tstamp = models.DateTimeField(blank=True, null=True)
    sensorname = models.TextField(blank=True, null=True)
    power_current = models.FloatField(blank=True, null=True)
    power_total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "power_data"
