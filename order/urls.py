from order.views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('add-to-cart/<str:dish_id>/<str:rest_id>/',customer_add_to_cart,name="add_to_cart"),
    path('view-cart/',customer_view_cart,name="view_cart"),
    path('del-item/<str:id>/',delete_item_from_cart,name="delete_from_cart"),
    path('order/',place_order,name="place_order"),
    path('payment/<str:method>/<str:order_id>/',order_payment,name="order_payment"),
    path('user-orders/',view_order,name="view_order"),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)