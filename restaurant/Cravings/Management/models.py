from django.db import models
import uuid
from django.contrib.auth.models import User



class MenuCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=30, null=False, blank=False)  

    def __str__(self):
        return f'{self.category_name} id {self.id}'


class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True)
    dishname = models.CharField(max_length=50, null=False, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  
    description = models.CharField(max_length=200, null=True, blank=True)  
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f'{self.dishname} - {self.price} {self.category} id {self.id}'


class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField(default=0, null=True, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'Table {self.number} - Capacity: {self.capacity} Available: {self.is_available} id {self.id}'


class TableReservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    reservation_date = models.DateTimeField(auto_now_add=True)
    number_of_people = models.PositiveIntegerField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)  

    def __str__(self):
        return f'Reservation for {self.customer} on {self.reservation_date} Table: {self.table} id {self.id}'


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reservation = models.ForeignKey(TableReservation, on_delete=models.CASCADE, related_name='orders')  
    items = models.ManyToManyField(MenuItem)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Order for {self.reservation.customer} on {self.reservation.reservation_date} id {self.id}'
    


