from django.urls import path
from . import views
from .views import *


urlpatterns =  [
    path('createMenuCategory',views.CreateMenuCategory.as_view(),name='createMenuCategory'),
    path('createMenuItem',views.CreateMenuItem.as_view(),name='createMenuItem'),
    path('createtable',views.Createtable.as_view(),name='createtable'),
    path('createTableReservation',views.CreateTableReservation.as_view(),name='CreateTableReservation'),
    path('CreateOrder',views.CreateOrder.as_view(),name='CreateOrder'),

]