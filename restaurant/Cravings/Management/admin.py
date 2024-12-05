from django.contrib import admin
from .models import*

admin.site.register(MenuCategory),
admin.site.register(MenuItem),
admin.site.register(Table),
admin.site.register(TableReservation),
admin.site.register(Order),

