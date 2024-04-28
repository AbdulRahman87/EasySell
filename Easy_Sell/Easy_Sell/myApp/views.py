from pyexpat import model
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Item, User_Details, Car, Mobile, Laptop, Bike, Item_Images, Feedback
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


# Create your views here.

def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'users': users})

def handleSignup(request):
    if request.method == 'POST':
        u_name = request.POST['u_name']
        f_name = request.POST['fname']
        l_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']

        check_user = User.objects.filter(username=u_name)
        check_email = User.objects.filter(email=email)
        if len(check_user) > 0:
            messages.error(request, 'Username already exist!')
            return redirect('Home')
        if len(check_email) > 0:
            messages.error(request, 'Email Already Exist!')
            return redirect('Home')

        password = request.POST['pass']
        user_img = request.FILES.get('user_img')

        newUser = User.objects.create_user(u_name, email, password)
        newUser.first_name = f_name
        newUser.last_name = l_name
        newUser.save()

        if user_img == None:
            _user = User_Details(_user=newUser, phone_no=phone)
            _user.save()
        else:
            _user = User_Details(_user = newUser, user_img=user_img, phone_no=phone)
            _user.save()
        messages.success(request, 'Your Account is created Successfully! Now you can login!')
        return redirect('Home')

def handleLogIn(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(username=user_name, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('Home')

def handleLogOut(request):
    logout(request)
    return redirect('Home')

def buyItem(request):
    if request.method == 'POST':
        option_value = request.POST['option_value']
        if option_value == 'car':
            price_range = int(request.POST['price_range'])
            driven_km = int(request.POST['driven_km'])
            body_type = request.POST['body_type']
            if body_type == 'all':
                if driven_km == 51000:
                    if price_range == 1100000:
                        cars = Car.objects.filter(item_price__gt=1000000, driven__gt=50000)
                    else:
                        cars = Car.objects.filter(item_price__lt=price_range, driven__gt=50000)
                else:
                    if price_range == 1100000:
                        cars = Car.objects.filter(item_price__gt=1000000, driven__lt=driven_km)
                    else:
                        cars = Car.objects.filter(item_price__lt=price_range, driven__lt=driven_km)
            else:
                if driven_km == 51000:
                    if price_range == 1100000:
                        cars = Car.objects.filter(item_price__gt=1000000, driven__gt=50000, car_type__icontains=body_type)
                    else:
                        cars = Car.objects.filter(item_price__lt=price_range, driven__gt=50000, car_type__icontains=body_type)
                else:
                    if price_range == 1100000:
                        cars = Car.objects.filter(item_price__gt=1000000, driven__lt=driven_km, car_type__icontains=body_type)
                    else:
                        cars = Car.objects.filter(item_price__lt=price_range, driven__lt=driven_km, car_type__icontains=body_type)
            return JsonResponse({'response': list(cars.values())})
        elif option_value == 'bike':
            price_range = int(request.POST['price_range'])
            driven_km = int(request.POST['driven_km'])
            if price_range == 110000:
                if driven_km == 51000:
                    bikes = Bike.objects.filter(item_price__gt=100000, driven__gt=50000)
                else:
                    bikes = Bike.objects.filter(item_price__gt=100000, driven__lt=driven_km)
            else:
                if driven_km == 51000:
                    bikes = Bike.objects.filter(item_price__lt=price_range, driven__gt=50000)
                else:
                    bikes = Bike.objects.filter(item_price__lt=price_range, driven__lt=driven_km)
            return JsonResponse({'response': list(bikes.values())})
        elif option_value == 'mobile':
            mobile_brand = request.POST['mobile_brand']
            price_range = int(request.POST['price_range'])
            ram_info = int(request.POST['ram_info'])
            if mobile_brand == 'all':
                if price_range == 21000:
                    if ram_info == 9:
                        mobiles = Mobile.objects.filter(item_price__gt=20000, ram__gt=8)
                    else:
                        mobiles = Mobile.objects.filter(item_price__gt=20000, ram=ram_info)
                else:
                    if ram_info == 9:
                        mobiles = Mobile.objects.filter(item_price__lt=price_range, ram__gt=8)
                    else:
                        mobiles = Mobile.objects.filter(item_price__lt=price_range, ram=ram_info)
            elif mobile_brand == 'apple':
                mobiles = Mobile.objects.filter(brand__icontains=mobile_brand)
            else:
                if price_range == 21000:
                    if ram_info == 9:
                        mobiles = Mobile.objects.filter(item_price__gt=20000, ram__gt=8, brand__icontains=mobile_brand)
                    else:
                        mobiles = Mobile.objects.filter(item_price__gt=20000, ram=ram_info, brand__icontains=mobile_brand)
                else:
                    if ram_info == 9:
                        mobiles = Mobile.objects.filter(item_price__lt=price_range, ram__gt=8, brand__icontains=mobile_brand)
                    else:
                        mobiles = Mobile.objects.filter(item_price__lt=price_range, ram=ram_info, brand__icontains=mobile_brand)
            return JsonResponse({'response': list(mobiles.values())})
        elif option_value == 'laptop':
            price_range = int(request.POST['price_range'])
            ram_info = int(request.POST['ram_info'])
            brand_info = request.POST['brand_info']
            processor = request.POST['processor']

            if brand_info == 'all':
                if price_range == 31000:
                    if ram_info == 17:
                        if processor == 'all':
                            laptops = Laptop.objects.filter(item_price__gt=30000, ram__gt=16)
                        else:
                            laptops = Laptop.objects.filter(item_price__gt=30000, ram__gt=16, processor__icontains=processor)
                    else:
                        if processor == 'all':
                            laptops = Laptop.objects.filter(item_price__gt=30000, ram=ram_info)
                        else:
                            laptops = Laptop.objects.filter(item_price__gt=30000, ram=ram_info, processor__icontains=processor)
                else:
                    if ram_info == 17:
                        if processor == 'all':
                            laptops = Laptop.objects.filter(item_price__lt=price_range, ram__gt=16)
                        else:
                            laptops = Laptop.objects.filter(item_price__lt=price_range, ram__gt=16, processor__icontains=processor)
                    else:
                        if processor == 'all':
                            laptops = Laptop.objects.filter(item_price__lt=price_range, ram=ram_info)
                        else:
                            laptops = Laptop.objects.filter(item_price__lt=price_range, ram=ram_info, processor__icontains=processor)
            elif brand_info == 'apple':
                if price_range == 31000:
                    if ram_info == 17:
                        laptops = Laptop.objects.filter(item_price__gt=30000, ram__gt=16, brand__icontains='apple')
                    else:
                        laptops = Laptop.objects.filter(item_price__gt=30000, ram=ram_info, brand__icontains='apple')
                else:
                    if ram_info == 17:
                        laptops = Laptop.objects.filter(item_price__lt=price_range, ram__gt=16, brand__icontains='apple')
                    else:
                        laptops = Laptop.objects.filter(item_price__lt=price_range, ram=ram_info, brand__icontains='apple')
            else:
                if price_range == 31000:
                    if ram_info == 17:
                        if processor == 'all':
                            laptops = Laptop.objects.filter(item_price__gt=30000, ram__gt=16, brand=brand_info)
                        else:
                            laptops = Laptop.objects.filter(item_price__gt=30000, ram__gt=16, processor__icontains=processor, brand=brand_info)
                    else:
                        if processor == 'all':
                            laptops = Laptop.objects.filter(item_price__gt=30000, ram=ram_info, brand=brand_info)
                        else:
                            laptops = Laptop.objects.filter(item_price__gt=30000, ram=ram_info, processor__icontains=processor, brand=brand_info)
                else:
                    if ram_info == 17:
                        if processor == 'all':
                            laptops = Laptop.objects.filter(item_price__lt=price_range, ram__gt=16, brand=brand_info)
                        else:
                            laptops = Laptop.objects.filter(item_price__lt=price_range, ram__gt=16, processor__icontains=processor, brand=brand_info)
                    else:
                        if processor == 'all':
                            laptops = Laptop.objects.filter(item_price__lt=price_range, ram=ram_info, brand=brand_info)
                        else:
                            laptops = Laptop.objects.filter(item_price__lt=price_range, ram=ram_info, processor__icontains=processor, brand=brand_info)
            return JsonResponse({'response': list(laptops.values())})
        elif option_value == 'other':
            item = Item.objects.filter(item_type__icontains='other')
            return JsonResponse({'response': list(item.values())})
    items = Item.objects.all().order_by('?')
    return render(request, 'items.html', {'items': items})

def Specific_item(request, item_name, item_id):
    item = Item.objects.get(item_name=item_name, id=item_id)
    if request.method == 'POST':
        item_images = request.FILES.getlist('item_images')
        for image in item_images:
            image_object = Item_Images(parent=item, item_img=image)
            image_object.save()
        return redirect(request.path_info)
    if item.item_type == 'CAR':
        _item = Car.objects.get(id=item_id)
        images = Item_Images.objects.filter(parent=_item)
    elif item.item_type == 'BIKE':
        _item = Bike.objects.get(id=item_id)
        images = Item_Images.objects.filter(parent=_item)
    elif item.item_type == 'MOBILE':
        _item = Mobile.objects.get(id=item_id)
        images = Item_Images.objects.filter(parent=_item)
    elif item.item_type == 'LAPTOP':
        _item = Laptop.objects.get(id=item_id)
        images = Item_Images.objects.filter(parent=_item)
    elif item.item_type == 'OTHER':
        _item = Item.objects.get(id=item_id)
        images = Item_Images.objects.filter(parent=_item)
    else:
        return redirect('Home')
    context = {'item_name': item_name, 'item': _item, 'images': images}
    return render(request, 'item.html', context)

def Recent_Items(request):
    if request.path_info[1:] == 'RecentCars':
        items = Car.objects.order_by('id').reverse()
        item_name = request.path_info[7:]
        return render(request, 'recent_items.html', {'items': items, 'item': item_name})
    elif request.path_info[1:] == 'RecentBikes':
        items = Bike.objects.order_by('id').reverse()
        item_name = request.path_info[7:]
        return render(request, 'recent_items.html', {'items': items, 'item': item_name})
    elif request.path_info[1:] == 'RecentMobiles':
        items = Mobile.objects.order_by('id').reverse()
        item_name = request.path_info[7:]
        return render(request, 'recent_items.html', {'items': items, 'item': item_name})
    elif request.path_info[1:] == 'RecentLaptops':
        items = Laptop.objects.order_by('id').reverse()
        item_name = request.path_info[7:]
        return render(request, 'recent_items.html', {'items': items, 'item': item_name})
    else:
        return redirect('Home')

def User_Profile(request, _user):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        detail = User_Details.objects.get(_user=request.user)
        detail.phone_no = phone
        detail.save()
        user_data = User.objects.get(username=request.user)
        user_data.first_name = first_name
        user_data.last_name = last_name
        user_data.email = email
        user_data.save()
        messages.success(request, 'Details has been updates Successfully!')
        return redirect(request.path_info)
    user = User.objects.get(username=_user)
    detail = User_Details.objects.get(_user=user)
    items = Item.objects.filter(item_owner=user)
    context = {'username': _user, 'user':user, 'detail': detail, 'items': items}
    return render(request, 'user_profile.html', context)

def update_pic(request):
    if request.method == 'POST':
        user_image = User_Details.objects.get(_user=request.user)
        image = request.FILES.get('image')
        user_image.user_img = image
        user_image.save()
        messages.success(request, 'Your profile pic updated Successfully!')
        return redirect(f'/user_profile/{request.user}')

def set_default_pic(request, user):
    try:
        user_object = User.objects.get(username=user)
        logged_in_user = request.user
        if user_object == logged_in_user:
            user_image = User_Details.objects.get(_user=request.user)
            user_image.user_img = 'IMG/user.png'
            user_image.save()
        else: 
            return redirect('Home')
    except Exception as e:
        return redirect('Home')
    return redirect(f'/user_profile/{user}')

def Sell_Item(request):
    if request.method == 'POST':
        item_type = request.POST['item_type']
        
        if item_type == 'CAR':
            car_name = request.POST['car_name']
            car_desc = request.POST['car_desc']
            car_model = request.POST['car_model']
            seats = request.POST['seats']
            sunroof = request.POST['sunroof']
            airbags = int(request.POST['airbags'])
            body = request.POST['body']
            fuel_type = request.POST['fuel_type']
            transmission = request.POST['transmission']
            car_top_speed = int(request.POST['car_top_speed'])
            car_driven = int(request.POST['car_driven'])
            car_power = int(request.POST['car_power'])
            car_age = request.POST['car_age']
            car_price = int(request.POST['car_price'])
            car_landing_img = request.FILES.get('car_landing_img')
            images = request.FILES.getlist('other_car_img')
            car = Car(item_owner=request.user, item_name=car_name, item_description=car_desc, item_type=item_type, item_landing_img=car_landing_img, item_price=car_price, model=car_model, age=car_age, Seats=seats, Air_Bags=airbags, Sunroof=sunroof, car_type=body, fuel_type=fuel_type, transmission=transmission, topSpeed=car_top_speed, driven=car_driven, power=car_power)
            car.save()
            if len(images) != 0:
                for image in images:
                    item_image = Item_Images(parent=car, item_img=image)
                    item_image.save()
            messages.success(request, f'Your item is ready to sell. <a href="ExploreItem/{car.item_name}/{car.id}">Click to see preview</a>')
            return redirect('SellYourItem')
        elif item_type == 'BIKE':
            bike_name = request.POST['bike_name']
            bike_desc = request.POST['bike_desc']
            bike_model = request.POST['bike_model']
            bike_top_speed = int(request.POST['bike_top_speed'])
            bike_driven = int(request.POST['bike_driven'])
            bike_power = int(request.POST['bike_power'])
            bike_age = request.POST['bike_age']
            bike_price = int(request.POST['bike_price'])
            bike_landing_img = request.FILES.get('bike_landing_img')
            images = request.FILES.getlist('other_bike_img')
            bike = Bike(item_owner=request.user, item_name=bike_name, item_description=bike_desc, item_type=item_type, item_landing_img=bike_landing_img, item_price=bike_price, model=bike_model, age=bike_age, topSpeed=bike_top_speed, driven=bike_driven, engine=bike_power)
            bike.save()
            if len(images) != 0:
                for image in images:
                    item_image = Item_Images(parent=bike, item_img=image)
                    item_image.save()
            messages.success(request, f'Your item is ready to sell. <a href="ExploreItem/{bike.item_name}/{bike.id}">Click to see preview</a>')
            return redirect('SellYourItem')
        elif item_type == 'MOBILE':
            mobile_name = request.POST['mobile_name']
            mobile_desc = request.POST['mobile_desc']
            mobile_model = request.POST['mobile_model']
            mobile_brand = request.POST['mobile_brand']
            ram = int(request.POST['mobile_ram'])
            rom = int(request.POST['mobile_rom'])
            battery = int(request.POST['mobile_battery'])
            processor = request.POST['mobile_processor']
            front_camera = int(request.POST['mobile_front_camera'])
            rear_camera = int(request.POST['mobile_rear_camera'])
            age = request.POST['mobile_age']
            price = int(request.POST['mobile_price'])
            screen_size = float(request.POST['mobile_screen_size'])
            m_landing_img = request.FILES.get('m_landing_img')
            m_other_img = request.FILES.getlist('m_other_img')
            mobile = Mobile(item_owner=request.user, item_name=mobile_name, item_description=mobile_desc, item_type=item_type, item_landing_img=m_landing_img, item_price=price, brand=mobile_brand, model=mobile_model, age=age, ram=ram, rom=rom, battery=battery, processor=processor, front_camera=front_camera, rear_camera=rear_camera, screen_size=screen_size)
            mobile.save()
            if len(m_other_img) != 0:
                for image in m_other_img:
                    item_image = Item_Images(parent=mobile, item_img=image)
                    item_image.save()
            messages.success(request, f'Your item is ready to sell. <a href="ExploreItem/{mobile.item_name}/{mobile.id}">Click to see preview</a>')
            return redirect('SellYourItem')
        elif item_type == 'LAPTOP':
            laptop_name = request.POST['laptop_name']
            laptop_desc = request.POST['laptop_desc']
            laptop_model = request.POST['laptop_model']
            laptop_brand = request.POST['laptop_brand']
            ram = int(request.POST['laptop_ram'])
            rom = int(request.POST['laptop_rom'])
            battery = int(request.POST['laptop_battery'])
            processor = request.POST['laptop_processor']
            age = request.POST['laptop_age']
            price = int(request.POST['laptop_price'])
            screen_size = float(request.POST['laptop_screen_size'])
            storage_type = request.POST['storage_type']
            wifi = request.POST['wifi']
            blutooth = request.POST['blutooth']
            touch_screen = request.POST['touch_screen']
            finger_print_sensor = request.POST['finger_print_sensor']
            laptop_landing_img = request.FILES.get('laptop_landing_img')
            other_laptop_img = request.FILES.getlist('other_laptop_img')
            laptop = Laptop(item_owner=request.user, item_name=laptop_name, item_description=laptop_desc, item_type=item_type, brand=laptop_brand, item_landing_img=laptop_landing_img, item_price=price, model=laptop_model, age=age, ram=ram, rom=rom, battery=battery, processor=processor, finger_print_sensor=finger_print_sensor, screen_size=screen_size, wifi=wifi, blutooth=blutooth, touch_screen=touch_screen, storage_type=storage_type)
            laptop.save()
            if len(other_laptop_img) != 0:
                for image in other_laptop_img:
                    item_image = Item_Images(parent=laptop, item_img=image)
                    item_image.save()
            messages.success(request, f'Your item is ready to sell. <a href="ExploreItem/{laptop.item_name}/{laptop.id}">Click to see preview</a>')
            return redirect('SellYourItem')
        else:
            item_name = request.POST['item_name']
            item_desc = request.POST['item_desc']
            item_price = request.POST['item_price']
            item_landing_img = request.FILES.get('item_landing_img')
            other_item_img = request.FILES.getlist('other_item_img')
            item = Item(item_name=item_name, item_description=item_desc, item_price=item_price, item_landing_img=item_landing_img, item_owner=request.user, item_type=item_type)
            item.save()
            if len(other_item_img) != 0:
                for image in other_item_img:
                    item_images = Item_Images(parent=item, item_img=image)
                    item_images.save()
            messages.success(request, f'Your item is ready to sell. <a href="ExploreItem/{item.item_name}/{item.id}">Click to see preview</a>')
            return redirect('SellYourItem')
    return render(request, 'sell_item.html')

def Contact(request):
    if request.method == 'POST':
        query = request.POST['query']
        feedback = Feedback(user=request.user, query=query)
        feedback.save()
        messages.success(request, 'Your Feedbak has been submitted. Thanks You!!!')
        return redirect('Contact')
    return render(request, 'contact.html')

def About(request):
    return render(request, 'about.html')

def editItem(request, item, item_type, item_id):
    if request.method == 'POST':
        if item_type == 'CAR':
            item = Car.objects.get(id=item_id)
            images = Item_Images.objects.filter(parent=item)
            item_name = request.POST['item_name']
            item_desc = request.POST['item_desc']
            item_model = request.POST['item_model']
            seats = request.POST['seats']
            airbags = request.POST['airbags']
            sunroof = request.POST['sunroof']
            body = request.POST['body']
            fuel_type = request.POST['fuel_type']
            transmission = request.POST['transmission']
            item_top_speed = request.POST['item_top_speed']
            item_driven = request.POST['item_driven']
            item_power = request.POST['item_power']
            item_age = request.POST['item_age']
            item_price = request.POST['item_price']
            item_landing_img = request.FILES.get('item_landing_img')
            if item_landing_img is None:
                item.item_name = item_name
                item.item_description = item_desc
                item.model = item_model
                item.seats = seats
                item.airbags = airbags
                item.sunroof = sunroof
                item.body = body
                item.fuel_type = fuel_type
                item.transmission = transmission
                item.topSpeed = item_top_speed
                item.driven = item_driven
                item.power = item_power
                item.age = item_age
                item.item_price = item_price
                item.save()
            else:
                item.item_name = item_name
                item.item_description = item_desc
                item.model = item_model
                item.seats = seats
                item.airbags = airbags
                item.sunroof = sunroof
                item.body = body
                item.fuel_type = fuel_type
                item.transmission = transmission
                item.topSpeed = item_top_speed
                item.driven = item_driven
                item.power = item_power
                item.age = item_age
                item.item_price = item_price
                item.item_landing_img = item_landing_img
                item.save()
            return redirect('Item', item_name=item.item_name, item_id=item.id)
        elif item_type == 'BIKE':
            item = Bike.objects.get(id=item_id)
            images = Item_Images.objects.filter(parent=item)
            item_name = request.POST['item_name']
            item_desc = request.POST['item_desc']
            item_model = request.POST['item_model']
            item_top_speed = request.POST['item_top_speed']
            item_driven = request.POST['item_driven']
            item_power = request.POST['item_engine']
            item_age = request.POST['item_age']
            item_price = request.POST['item_price']
            item_landing_img = request.FILES.get('item_landing_img')
            if item_landing_img is None:
                item.item_name = item_name
                item.item_description = item_desc
                item.model = item_model
                item.topSpeed = item_top_speed
                item.driven = item_driven
                item.engine = item_power
                item.age = item_age
                item.item_price = item_price
                item.save()
            else:
                item.item_name = item_name
                item.item_description = item_desc
                item.model = item_model
                item.topSpeed = item_top_speed
                item.driven = item_driven
                item.engine = item_power
                item.age = item_age
                item.item_price = item_price
                item.item_landing_img = item_landing_img
                item.save()
            return redirect('Item', item_name=item.item_name, item_id=item.id)
        elif item_type == 'MOBILE':
            item = Mobile.objects.get(id=item_id)
            images = Item_Images.objects.filter(parent=item)
            item_name = request.POST['item_name']
            item_desc = request.POST['item_desc']
            item_model = request.POST['item_model']
            item_ram = request.POST['item_ram']
            item_rom = request.POST['item_rom']
            item_processor = request.POST['item_processor']
            item_screen_size = request.POST['item_screen_size']
            item_front_camera = request.POST['item_front_camera']
            item_rear_camera = request.POST['item_rear_camera']
            item_brand = request.POST['item_brand']
            item_battery = request.POST['item_battery']
            item_age = request.POST['item_age']
            item_price = request.POST['item_price']
            item_landing_img = request.FILES.get('item_landing_img')
            if item_landing_img is None:
                item.item_name = item_name
                item.item_description = item_desc
                item.model = item_model
                item.ram = item_ram
                item.rom = item_rom
                item.brand = item_brand
                item.battery = item_battery
                item.processor = item_processor
                item.screen_size = item_screen_size
                item.front_camera = item_front_camera
                item.rear_camera = item_rear_camera
                item.age = item_age
                item.item_price = item_price
                item.save()
            else:
                item.item_name = item_name
                item.item_description = item_desc
                item.model = item_model
                item.ram = item_ram
                item.rom = item_rom
                item.brand = item_brand
                item.battery = item_battery
                item.processor = item_processor
                item.screen_size = item_screen_size
                item.front_camera = item_front_camera
                item.rear_camera = item_rear_camera
                item.age = item_age
                item.item_price = item_price
                item.item_landing_img = item_landing_img
                item.save()
            return redirect('Item', item_name=item.item_name, item_id=item.id)
        elif item_type == 'LAPTOP':
            item = Laptop.objects.get(id=item_id)
            images = Item_Images.objects.filter(parent=item)
            item_name = request.POST['item_name']
            item_desc = request.POST['item_desc']
            item_model = request.POST['item_model']
            item_ram = request.POST['item_ram']
            item_rom = request.POST['item_rom']
            item_processor = request.POST['item_processor']
            item_screen_size = request.POST['item_screen_size']
            finger_print_sensor = request.POST['finger_print_sensor']
            touch_screen = request.POST['touch_screen']
            wifi = request.POST['wifi']
            blutooth = request.POST['blutooth']
            storage_type = request.POST['storage_type']
            item_brand = request.POST['item_brand']
            item_battery = request.POST['item_battery']
            item_age = request.POST['item_age']
            item_price = request.POST['item_price']
            item_landing_img = request.FILES.get('item_landing_img')
            if item_landing_img is None:
                item.item_name = item_name
                item.item_description = item_desc
                item.model = item_model
                item.ram = item_ram
                item.rom = item_rom
                item.brand = item_brand
                item.battery = item_battery
                item.processor = item_processor
                item.screen_size = item_screen_size
                item.finger_print_sensor = finger_print_sensor
                item.storage_type = storage_type
                item.touch_screen = touch_screen
                item.wifi = wifi
                item.blutooth = blutooth
                item.age = item_age
                item.item_price = item_price
                item.save()
            else:
                item.item_name = item_name
                item.item_description = item_desc
                item.model = item_model
                item.ram = item_ram
                item.rom = item_rom
                item.brand = item_brand
                item.battery = item_battery
                item.processor = item_processor
                item.screen_size = item_screen_size
                item.finger_print_sensor = finger_print_sensor
                item.storage_type = storage_type
                item.touch_screen = touch_screen
                item.wifi = wifi
                item.blutooth = blutooth
                item.age = item_age
                item.item_price = item_price
                item.item_landing_img = item_landing_img
                item.save()
            return redirect('Item', item_name=item.item_name, item_id=item.id)
        else:
            item = Item.objects.get(id=item_id)
            images = Item_Images.objects.filter(parent=item)
            item_name = request.POST['item_name']
            item_desc = request.POST['item_desc']
            item_price = request.POST['item_price']
            item_landing_img = request.FILES.get('item_landing_img')
            if item_landing_img is None:
                item.item_name = item_name
                item.item_description = item_desc
                item.item_price = item_price
                item.save()
            else:
                item.item_name = item_name
                item.item_description = item_desc
                item.item_price = item_price
                item.item_landing_img = item_landing_img
                item.save()
            return redirect('Item', item_name=item.item_name, item_id=item.id)
    else:
        if item_type == 'CAR':
            item = Car.objects.get(id=item_id)
            images = Item_Images.objects.filter(parent=item)
        elif item_type == 'BIKE':
            item = Bike.objects.get(id=item_id)
            images = Item_Images.objects.filter(parent=item)
        elif item_type == 'MOBILE':
            item = Mobile.objects.get(id=item_id)
            images = Item_Images.objects.filter(parent=item)
        elif item_type == 'LAPTOP':
            item = Laptop.objects.get(id=item_id)
            images = Item_Images.objects.filter(parent=item)
        else:
            item = Item.objects.get(id=item_id)
            images = Item_Images.objects.filter(parent=item)
        if item.item_owner != request.user:
            return redirect('Home')
        context = {'item': item, 'images': images}
        return render(request, 'edit_item.html', context)

def deleteImages(request):
    if request.method == 'POST':
        ids = request.POST['img_ids']
        parameters = request.POST['parameters'].split(',')
        img_ids = ids.split(',')
        i = 0
        while(i<len(img_ids)):
            Item_Images.objects.get(id=img_ids[i]).delete()
            i += 1
        return redirect('Item', item_name=parameters[0], item_id=parameters[1])

def deleteItem(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.user == item.item_owner:
        item_name = item.item_name
        item.delete()
        messages.success(request, f'{item_name} has been deleted!')
        return redirect('Home')
    else:
        return redirect('Home')