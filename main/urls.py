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
    path('logout/',logout_page,name="logout_session"),
    path('restaurant-home/',restaurant_home,name="rest_home"),
    path('restaurant-menu/',restaurant_display_menu,name="display_menu"),
    path('restaurant-add-menu/',restaurant_addTo_menu,name="add_menu"),
    
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)