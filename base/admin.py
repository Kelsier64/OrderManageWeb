from django.contrib import admin

# Register your models here.
from .models import ExtendedUser

from .models import Order,Product,Announcement
admin.site.register(ExtendedUser)

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Announcement)

