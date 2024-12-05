from rest_framework.views import  APIView
from rest_framework.response import Response
from . models import *
from . response_serializers import *
from .models import TableReservation
from django.contrib.auth.models import User
from rest_framework import status
from .model_helper import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json
import uuid
import logging


class CreateMenuCategory(APIView):
    def post(self,request):
        data = request.data
        try:
            menu = MenuCategory.objects.create(category_name = data['category_name'])
            serializer  = MenuCategorySerializers(menu).data
            return Response(serializer,status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(f'cannot able to create{error}')
        
        
class CreateMenuItem(APIView):
    def post(self,request):
        data = request.data
        try:    
            menuCategory = MenuCategory.objects.create(category_name = data['category_name'])
            menuItem = MenuItem.objects.create(
                                            category=menuCategory,
                                            dishname = data['dishname'],
                                            price = data['price'],
                                            description = data['description'],
                                            )
            serializer = MenuitemSerializers(menuItem).data
            return Response(serializer,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f'Cannot able to create{e}')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    
class Createtable(APIView):
    def post(self,request):
        data = request.data
        try:
            table = Table.objects.create(
                                        number = data['number'],
                                        capacity = data['capacity'],
                                        is_available = data['True']
                                        )
            serializer = TableSerializers(table).data
            return Response(serializer,status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(f'cannot able to create{error}')  
        
        
class CreateTableReservation(APIView):
    def post(self,request):
        try:
            data = request.data
            table = Table.objects.create(number = data['number'])
            user = User.objects.create(username = data['username'])
            tablereservation = TableReservation.objects.create(
                                                                table=table,
                                                                customer=user,
                                                                reservation_date = data['reservation_date'],
                                                                number_of_people = data['number_of_people'],
                                                                contact_number = data['contact_number'])                                      
            serializer = TableReservation(tablereservation)
            return Response(serializer,status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(f'cannot able to create{error}')
         

class CreateOrder(APIView):
    def post(self, request):
        data = request.data
        reservation = TableReservation.objects.get(id=data["reservation_id"])
        print(reservation.id)
        items = MenuItem.objects.create(category_name=data['items']['category_name']).all()
        order = Order.objects.create(
                                    items=items,
                                    reservation=reservation,
                                    total_amount=data['total_amount'])
        order.items.set(items)
        return Response('created succesfully')
    


GST_PERCENTAGE = 18

class CreateOrder(APIView):
    def post(self, request):
        logging.debug(f"Request body: {request.body}")
        try:
          
            data = request.data
            
           
            if 'reservation_id' not in data or 'items' not in data:
                return Response({"error": "reservation_id and items are required fields."}, status=status.HTTP_400_BAD_REQUEST)

           
            reservation_id = str(data["reservation_id"])
            reservation_uuid = uuid.UUID(reservation_id)  

       
            reservation = TableReservation.objects.get(id=reservation_uuid)

            total_amount = 0
            order_items = []

           
            for item_data in data["items"]:
                dishname = item_data["dishname"]
                quantity = item_data["quantity"]

             
                menu_item = MenuItem.objects.get(dishname=dishname)
                item_total = menu_item.price * quantity
                total_amount += item_total
                order_items.append((menu_item, quantity, item_total))

            gst_amount = (total_amount * GST_PERCENTAGE) / 100
            total_with_gst = total_amount + gst_amount

        
            order = Order.objects.create(
                reservation=reservation,
                total_amount=total_with_gst
            )

            order_items_to_save = [item[0] for item in order_items]
            order.items.set(order_items_to_save)

          
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)

            
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, 680, "Order Summary")
            pdf.drawString(100, 660, f"Order ID: {order.id}")
            pdf.drawString(100, 640, f"Customer: {reservation.customer.username}")
            pdf.drawString(100, 620, f"Reservation Date: {reservation.reservation_date}")

            pdf.drawString(100, 600, "Items:")
            y_position = 580
            for item in order_items:
                pdf.drawString(120, y_position, f"{item[0].dishname} x {item[1]} @ {item[0].price} each = {item[2]}")
                y_position -= 20
            
        
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(100, y_position - 20, f"Subtotal: {total_amount}")
            pdf.drawString(100, y_position - 40, f"GST ({GST_PERCENTAGE}%): {gst_amount}")
            pdf.drawString(100, y_position - 60, f"Total Amount: {total_with_gst}")

            pdf.setFont("Helvetica", 10)
            pdf.drawString(100, y_position - 100, "Thank you for dining with us!")

            pdf.save()
            buffer.seek(0)

            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="order_{order.id}_bill.pdf"'
            return response

        except json.JSONDecodeError as e:
            return Response({"error": f"Invalid JSON format: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"error": f"Resource not found: {str(e)}"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    
# class CreateOrder(APIView):
#     def post(self, request):
#         data = request.data

#         try:
            
#             reservation = TableReservation.objects.get(id=data["reservation_id"])
            
          
#             total_amount = 0
            
          
#             order_items = []

    
#             for item_data in data["items"]:
#                 dishname = item_data["dishname"]
#                 quantity = item_data["quantity"]

          
#                 menu_item = MenuItem.objects.get(dishname=dishname)
                
               
#                 item_total = menu_item.price * quantity
#                 total_amount += item_total
                
             
#                 order_items.append((menu_item, quantity, item_total))

#             order = Order.objects.create(
#                 reservation=reservation,
#                 total_amount=total_amount
#             )

         
#             order_items_to_save = [item[0] for item in order_items]
#             order.items.set(order_items_to_save)

           
#             response_data = {
#                 "order_id": order.id,
#                 "customer": reservation.customer.username,
#                 "reservation_date": reservation.reservation_date,
#                 "items": [
#                     {
#                         "dish_name": item[0].dishname,
#                         "quantity": item[1],
#                         "price_per_unit": item[0].price,
#                         "total_cost": item[2]
#                     }
#                     for item in order_items
#                 ],
#                 "total_amount": total_amount
#             }
            
#             return Response(response_data, status=status.HTTP_201_CREATED)

#         except TableReservation.DoesNotExist:
#             return Response({"error": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)
#         except MenuItem.DoesNotExist:
#             return Response({"error": f"Menu item '{dishname}' not found."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as error:
#             return Response({"error": f"An error occurred: {error}"}, status=status.HTTP_400_BAD_REQUEST)


        

    



    


                    


                
                    




       

            


