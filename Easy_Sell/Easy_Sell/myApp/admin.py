from django.contrib import admin
from .models import User_Details, Item, Car, Bike, Mobile, Laptop, Item_Images, Feedback

# Register your models here.

admin.site.register(User_Details)
admin.site.register(Item)
admin.site.register(Car)
admin.site.register(Bike)
admin.site.register(Mobile)
admin.site.register(Laptop)
admin.site.register(Item_Images)
admin.site.register(Feedback)