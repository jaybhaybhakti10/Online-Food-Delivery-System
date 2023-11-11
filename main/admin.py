from django.contrib import admin
from . import models

admin.site.register(models.Customer)
admin.site.register(models.Restaurant)
admin.site.register(models.Delivery_Agent)
admin.site.register(models.Address_Book)
admin.site.register(models.Menu)
