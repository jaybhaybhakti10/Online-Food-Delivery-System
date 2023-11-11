from main.views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('',login_user,name="login_page"),
    path('login/',login_user,name="login_page"),
    path('register/',register_user,name="registration_page"),
    path('logout/',logout_page,name="logout_session"),
    
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)