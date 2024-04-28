from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Home"),
    path('handleSignUp', views.handleSignup, name="HandleSignUp"),
    path('handleLogIn', views.handleLogIn, name="handleLogIn"),
    path('handleLogOut', views.handleLogOut, name="handleLogOut"),
    path('ExploreItems', views.buyItem, name="ExploreItems"),
    path('ExploreItem/<str:item_name>/<int:item_id>', views.Specific_item, name="Item"),
    path('RecentCars', views.Recent_Items, name="RecentCars"),
    path('RecentBikes', views.Recent_Items, name="RecentBikes"),
    path('RecentMobiles', views.Recent_Items, name="RecentMobiles"),
    path('RecentLaptops', views.Recent_Items, name="RecentLaptops"),
    path('user_profile/<str:_user>', views.User_Profile, name="UserProfile"),
    path('updateUserProfilePic', views.update_pic, name="UpdateProfilePic"),
    path('set_as_default_pic/<str:user>', views.set_default_pic, name="SetDefaultProfilePic"),
    path('SellYourItem', views.Sell_Item, name="SellYourItem"),
    path('ContactUs', views.Contact, name="Contact"),
    path('AboutUs', views.About, name="About"),
    path('editItem/<str:item>/<str:item_type>/<str:item_id>', views.editItem, name="EditItem"),
    path('deleteImages', views.deleteImages, name="DeleteImages"),
    path('deleteItem/<str:item_id>', views.deleteItem, name="DeleteItem")
]