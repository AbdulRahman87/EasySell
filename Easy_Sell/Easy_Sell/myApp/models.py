from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_Details(models.Model):
    _user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_no = models.CharField(max_length=12, default='Not Available')
    user_img = models.ImageField(upload_to='user_img/images', default='IMG/user.png', null=False, blank=False)

    def __str__(self):
        return self._user.first_name

class Item(models.Model):
    item_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, default=None)
    item_description = models.TextField()
    item_type = models.CharField(max_length=255)
    item_landing_img = models.ImageField(upload_to='item_img/images', default=None, null=False, blank=False)
    item_price = models.IntegerField()

    def __str__(self):
        return self.item_name

class Car(Item):
    model = models.CharField(max_length=255)
    age = models.DateField()
    Seats = models.CharField(max_length=255, default=None)
    Air_Bags = models.IntegerField(default=0)
    Sunroof = models.CharField(max_length=5)
    car_type = models.CharField(max_length=255, default=None)
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    topSpeed = models.IntegerField(default=100)
    driven = models.IntegerField()
    power = models.IntegerField()

class Bike(Item):
    model = models.CharField(max_length=255)
    age = models.DateField()
    topSpeed = models.IntegerField(default=80)
    driven = models.IntegerField()
    engine = models.IntegerField()

class Mobile(Item):
    brand = models.CharField(max_length=255, default=None)
    model = models.CharField(max_length=255)
    age = models.DateField()
    ram = models.IntegerField(default=2)
    rom = models.IntegerField(default=16)
    battery = models.IntegerField(default=3500)
    processor = models.CharField(max_length=255)
    front_camera = models.IntegerField(default=2)
    rear_camera = models.IntegerField(default=8)
    screen_size = models.FloatField(default=5)

class Laptop(Item):
    brand = models.CharField(max_length=255, default=None)
    model = models.CharField(max_length=255)
    age = models.DateField()
    ram = models.IntegerField(default=2)
    rom = models.IntegerField(default=64)
    battery = models.IntegerField(default=3500)
    processor = models.CharField(max_length=255)
    finger_print_sensor = models.CharField(max_length=5)
    touch_screen = models.CharField(max_length=5)
    wifi = models.CharField(max_length=5)
    blutooth = models.CharField(max_length=5)
    screen_size = models.FloatField(default=14)
    storage_type = models.CharField(max_length=5)

class Item_Images(models.Model):
    parent = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_img = models.ImageField(upload_to='item_img/images', null=False, blank=False)

    def __str__(self):
        return self.parent.item_name

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()

    def __str__(self):
        return self.user.first_name