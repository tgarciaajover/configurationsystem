from django.db import models
from django.utils import timezone

# Create your models here.
class MeasuringEntityStatusInterval(models.Model):
    id_owner = models.IntegerField(default=0)
    owner_type = models.IntegerField(default=0)
    datetime_to = models.DateTimeField(default=timezone.now)
    datetime_from = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=150, blank=True)
    related_object = models.IntegerField(blank=True, null=True)
    related_object_type = models.IntegerField(blank=True, null=True)
    reason_code = models.CharField(max_length=150, blank=True, null=True)
    executed_object_canonical = models.CharField(max_length=300, blank=True)
    production_rate = models.DecimalField(max_digits=16, decimal_places=4, default=0.0)
    conversion_1 = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    conversion_2 = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    actual_production_rate = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    qty_defective = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)

    class Meta:
        db_table = 'measuringentitystatusinterval'

class MeasuredAttributeValue(models.Model):
    id_owner = models.IntegerField(default=0)
    owner_type = models.IntegerField(default=0)
    attribute_name = models.CharField(max_length=300, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    value_decimal = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    value_datetime = models.DateTimeField(blank=True, null=True)
    value_string = models.TextField(blank=True, null=True)
    value_int = models.IntegerField(blank=True, null=True)
    value_boolean = models.NullBooleanField()
    value_date = models.DateField(blank=True, null=True)
    value_time = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'measuredattributevalue'