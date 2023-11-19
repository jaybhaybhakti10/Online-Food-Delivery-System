from order.views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('add-to-cart/<str:dish_id>/<str:rest_id>/',customer_add_to_cart,name="add_to_cart"),
    path('view-cart/',customer_view_cart,name="view_cart"),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)