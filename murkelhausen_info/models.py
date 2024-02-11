# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BodyBattery(models.Model):
    tstamp = models.DateTimeField(primary_key=True)
    body_battery_status = models.CharField(blank=True, null=True)
    body_battery_level = models.IntegerField(blank=True, null=True)
    body_battery_version = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'body_battery'


class BodyBatteryActivityEvent(models.Model):
    tstamp_start = models.DateTimeField(primary_key=True)
    event_type = models.CharField()
    duration_seconds = models.IntegerField()
    body_battery_impact = models.IntegerField()
    feedback_type = models.CharField()
    short_feedback = models.CharField()

    class Meta:
        managed = False
        db_table = 'body_battery_activity_event'


class BodyBatteryDaily(models.Model):
    calendar_date = models.DateField(primary_key=True)
    charged = models.IntegerField(blank=True, null=True)
    drained = models.IntegerField(blank=True, null=True)
    dynamic_feedback_event = models.TextField()  # This field type is a guess.
    end_of_day_dynamic_feedback_event = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'body_battery_daily'


class Floors(models.Model):
    tstamp_start = models.DateTimeField(primary_key=True)
    tstamp_end = models.DateTimeField()
    floorsascended = models.IntegerField(db_column='floorsAscended')  # Field name made lowercase.
    floorsdescended = models.IntegerField(db_column='floorsDescended')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'floors'


class HeartRate(models.Model):
    tstamp = models.DateTimeField(primary_key=True)
    heart_rate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'heart_rate'


class HeartRateDaily(models.Model):
    measure_date = models.DateField(primary_key=True)
    resting_heart_rate = models.IntegerField(blank=True, null=True)
    min_heart_rate = models.IntegerField(blank=True, null=True)
    max_heart_rate = models.IntegerField(blank=True, null=True)
    last_seven_days_avg_resting_heart_rate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'heart_rate_daily'


class SleepBodyBattery(models.Model):
    tstamp = models.DateTimeField(primary_key=True)
    body_battery_level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sleep_body_battery'


class SleepDaily(models.Model):
    calendar_date = models.DateField(primary_key=True)
    sleep_time_seconds = models.IntegerField(blank=True, null=True)
    nap_time_seconds = models.IntegerField(blank=True, null=True)
    sleep_start_tstamp = models.DateTimeField(blank=True, null=True)
    sleep_end_tstamp = models.DateTimeField(blank=True, null=True)
    unmeasurable_sleep_seconds = models.IntegerField(blank=True, null=True)
    deep_sleep_seconds = models.IntegerField(blank=True, null=True)
    light_sleep_seconds = models.IntegerField(blank=True, null=True)
    rem_sleep_seconds = models.IntegerField(blank=True, null=True)
    awake_sleep_seconds = models.IntegerField(blank=True, null=True)
    average_sp_o_2_value = models.FloatField(blank=True, null=True)
    lowest_sp_o_2_value = models.FloatField(blank=True, null=True)
    highest_sp_o_2_value = models.FloatField(blank=True, null=True)
    average_sp_o_2_hrsleep = models.FloatField(blank=True, null=True)
    average_respiration_value = models.FloatField(blank=True, null=True)
    lowest_respiration_value = models.FloatField(blank=True, null=True)
    highest_respiration_value = models.FloatField(blank=True, null=True)
    awake_count = models.IntegerField(blank=True, null=True)
    avg_sleep_stress = models.FloatField(blank=True, null=True)
    sleep_score_feedback = models.CharField(blank=True, null=True)
    sleep_score_insight = models.CharField(blank=True, null=True)
    sleep_score_personalized_insight = models.CharField(blank=True, null=True)
    restless_moments_count = models.IntegerField(blank=True, null=True)
    avg_overnight_hrv = models.FloatField(blank=True, null=True)
    hrv_status = models.CharField(blank=True, null=True)
    body_battery_change = models.IntegerField(blank=True, null=True)
    resting_heart_rate = models.IntegerField(blank=True, null=True)
    sleep_scores = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sleep_daily'


class SleepHeartRate(models.Model):
    tstamp = models.DateTimeField(primary_key=True)
    heart_rate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sleep_heart_rate'


class SleepHrvData(models.Model):
    tstamp = models.DateTimeField(primary_key=True)
    hrv_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sleep_hrv_data'


class SleepLevels(models.Model):
    tstamp_start = models.DateTimeField(primary_key=True)
    tstamp_end = models.DateTimeField()
    activity_level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sleep_levels'


class SleepMovement(models.Model):
    tstamp_start = models.DateTimeField(primary_key=True)
    tstamp_end = models.DateTimeField()
    activity_level = models.FloatField()

    class Meta:
        managed = False
        db_table = 'sleep_movement'


class SleepRespirationData(models.Model):
    tstamp = models.DateTimeField(primary_key=True)
    respiration_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sleep_respiration_data'


class SleepRestlessMoments(models.Model):
    tstamp = models.DateTimeField(primary_key=True)
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sleep_restless_moments'


class SleepSpo2Data(models.Model):
    tstamp = models.DateTimeField(primary_key=True)
    epoch_duration = models.IntegerField(blank=True, null=True)
    spo2_value = models.IntegerField(blank=True, null=True)
    reading_confidence = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sleep_spo2_data'


class SleepStress(models.Model):
    tstamp = models.DateTimeField(primary_key=True)
    stress_level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sleep_stress'


class Steps(models.Model):
    tstamp_start = models.DateTimeField(primary_key=True)
    tstamp_end = models.DateTimeField()
    steps = models.IntegerField()
    pushes = models.IntegerField()
    primaryactivitylevel = models.CharField(db_column='primaryActivityLevel')  # Field name made lowercase.
    activitylevelconstant = models.BooleanField(db_column='activityLevelConstant')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'steps'


class StepsDaily(models.Model):
    calendar_date = models.DateField(primary_key=True)
    total_steps = models.IntegerField(blank=True, null=True)
    total_distance = models.IntegerField(blank=True, null=True)
    step_goal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'steps_daily'


class Stress(models.Model):
    tstamp = models.DateTimeField(primary_key=True)
    stress_level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stress'


class StressDaily(models.Model):
    calendar_date = models.DateField(primary_key=True)
    max_stress_level = models.IntegerField(blank=True, null=True)
    avg_stress_level = models.IntegerField(blank=True, null=True)
    stress_chart_value_offset = models.IntegerField(blank=True, null=True)
    stress_chart_y_axis_origin = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stress_daily'
