from django.db import models


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    order_num = models.CharField(max_length=10)
    price_dollar = models.FloatField()
    delivery_data = models.CharField(max_length=20)
    price_rub = models.FloatField()
