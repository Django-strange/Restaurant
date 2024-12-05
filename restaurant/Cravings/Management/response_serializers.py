from rest_framework import serializers
from. models import*
from django.contrib.auth.models import User



class MenuCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['category_name']

class MenuitemSerializers(serializers.ModelSerializer):

  
    category=serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = '__all__'

    def get_category(self,obj):
        return{'category_name':obj.category.category_name}


class TableSerializers(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['number','capacity','is_available']

class TableReservation(serializers.ModelSerializer):

  
    table = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    

    class Meta:
        model = TableReservation
        fields = ['table','customer','reservation_date','number_of_people','contact_number']

 
    def get_table(self,obj):
        return{'number':obj.table.number}
    def get_customer(self,obj): 
        return{'username':obj.customer.user.username}
    


    





   
    



    
    



