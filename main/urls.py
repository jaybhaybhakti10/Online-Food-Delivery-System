from main.views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('',home,name="home_page"),
    path('login-user/',login_user,name="login_customer"),
    path('login-restaurant/',login_restaurant,name="login_restaurant"),
    path('login-rider/',login_rider,name="login_delivery"),
    path('register-user/',register_user,name="registration_customer"),
    path('register-restaurant/',register_restaurant,name="registration_restaurant"),
    path('register-rider/',register_rider,name="registration_delivery"),
    path('logout-restaurant/',logout_restaurant,name="logout_restaurant"),
    path('logout-user/',logout_user,name="logout_customer"),
    path('logout-rider/',logout_rider,name="logout_rider"),
    # restuarnt urls
    path('restaurant-home/',restaurant_home,name="rest_home"),
    path('restaurant-menu/',restaurant_display_menu,name="display_menu"),
    path('restaurant-add-menu/',restaurant_addTo_menu,name="add_menu"),
    path('restaurant-profile/',restaurant_profile,name="rest_profile"),
    path('restaurant-edit-profile/',restaurant_edit_profile,name="edit_restaurant"),
    path('restaurant-change-password/',restaurant_change_password,name="rest_change_password"),
    path('edit-dish/<str:dishId>/',restaurant_edit_dish,name="edit_dish"),
    path('delete-dish/<str:dishId>/',restaurant_delete_dish,name="delete_dish"),
    # customer urls
    path('user-home/',customer_home,name="cust_home"),
    path('user-profile/',customer_profile,name="cust_profile"),
    path('user-profile-edit/',customer_profile_edit,name="cust_profile_edit"),
    path('user-change-password/',customer_change_password,name="cust_change_password"),
    path('user-add-address/',customer_add_address,name="cust_add_address"),
    path('user-edit-address/<str:type>/',customer_edit_address,name="cust_edit_address"),
    path('user-delete-address/<str:type>/',customer_delete_address,name="cust_delete_address"),
    path('user-view-menu/<str:restId>/',customer_view_menu,name="cust_view_menu"),
    path('user-view-veg/<str:restId>/',customer_view_veg,name="cust_view_veg"),
    path('user-view-nonveg/<str:restId>/',customer_view_nonveg,name="cust_view_non_veg"),
    
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)