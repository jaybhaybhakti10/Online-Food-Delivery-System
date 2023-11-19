from django.db import models
from main.models import *


        
class Cart(models.Model):
    item=models.ForeignKey(Menu,on_delete=models.CASCADE)
    cust_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
    item_count=models.IntegerField()
    amount=models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False,default=0.00)
    def __str__(self):
        return self.cust_id.customer_name
    
    class Meta:
        verbose_name="cart"


# order table
class Order(models.Model):
    order_id=models.CharField(max_length=100,primary_key=True)
    rest_id=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    cust_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
    rider_id=models.OneToOneField(Delivery_Agent,on_delete=models.SET_NULL,blank=True,null=True)
    cart_item=models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True)
    address_of_delivery=models.ForeignKey(Address_Book,on_delete=models.CASCADE)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    status_of_delivery=models.CharField(max_length=100,null=False,blank=False)
    
    def __str__(self):
        return self.order_id
    
    class Meta:
        verbose_name="order"
        
    def save(self, *args, **kwargs):
        # Check if the status is 'ordered' or 'delivered' and rider_id is null
        if self.status_of_delivery in ['ORDERED', 'DELIVERED'] and not self.rider_id:
            raise ValueError("Rider has to be assigned")

        super(Order, self).save(*args, **kwargs)

# payment table
class Payment(models.Model):
    order_id=models.OneToOneField(Order,on_delete=models.CASCADE)
    payment_method=models.CharField(max_length=100)
    payment_status=models.CharField(max_length=100,null=False,blank=False)
    payment_date=models.DateField()
    payment_time=models.TimeField()
    transaction_id=models.CharField(max_length=100,primary_key=True)
    
    def __str__(self):
        return self.transaction_id
    class Meta:
        verbose_name="payment"
    
# rateing/reviews table   
class Reviews(models.Model):
    cust_id=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    rest_id=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    rating=models.DecimalField(max_digits=3, decimal_places=1)
    review=models.TextField(max_length=255)

    def __str__(self):
        return self.rest_id.restaurant_name
    
    class Meta:
        verbose_name="rating and reviews"
    
    
    


    
    
    
