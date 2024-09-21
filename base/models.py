from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    release_date = models.DateField(blank=True, null=True)
    platform = models.CharField(max_length=10)
    product_name = models.CharField(max_length=50)
    suggested_price = models.DecimalField(max_digits=7, decimal_places=0,blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    user_class = models.CharField(max_length=20)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')  # 關聯到商品表的外鍵
    create_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)  # 訂單的備註
    quantity = models.IntegerField()  # 訂單中的商品數量
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='orders',blank=True, null=True)

class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    notes = models.TextField(blank=True, null=True)



