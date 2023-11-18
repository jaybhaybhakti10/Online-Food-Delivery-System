from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist

User=get_user_model()
        
        


# Model for customer
class Customer(models.Model):
    # user includes : email,phone number and password
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    customer_name=models.CharField(max_length=100)
    dob=models.DateField()
    age=models.PositiveIntegerField()
    cust_id=models.CharField(max_length=100,primary_key=True)
    
    def calculate_age(self):
        today=datetime.date.today()
        age=today.year-self.dob.year - ((today.month,today.day)<(self.dob.month,self.dob.day))
        self.age=age
    
    def save(self,*args,**kwargs):
        self.calculate_age()
        super(Customer,self).save(*args,**kwargs)
        
    def __str__(self):
        return self.customer_name
    
    class Meta:
        verbose_name="customer"
        unique_together=('user','cust_id')
    
    


# Model for restaurant
# class Restaurant:
#     # user includes : email,phone number and password
#     user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
#     restaurant_name=models.CharField(max_length=100)
#     GSTIN_num=models.CharField(max_length=15,unique=True,null=False,primary_key=True)
#     # fileds to store restaurant timings
#     start_time=models.TimeField()
#     end_time=models.TimeField()
    
#     # fields to store address
#     house=models.CharField(max_length=100)
#     street_address=models.CharField(max_length=255)
#     city=models.CharField(max_length=100)
#     state=models.CharField(max_length=100)
#     pin_code=models.CharField(max_length=6)
    
#     def clean(self):
#         if self.start_time >= self.end_time:
#             raise ValidationError("End time must be greater than start time.")
    
#     def __str__(self):
#         return self.restaurant_name
    
#     class Meta:
#         verbose_name="restaurant"
#         unique_together=('user','GSTIN_num')
#         constraints = [
#             models.CheckConstraint(check=models.Q(end_time__gt=models.F('start_time')), name='end_time_gt_start_time')
#         ]
    

class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    restaurant_name = models.CharField(max_length=100)
    GSTIN_num = models.CharField(max_length=15, unique=True, null=False, primary_key=True)
    restaurant_image=models.ImageField(upload_to="restImages/",max_length=255,null=True,blank=True,default=None)


    # Fields to store restaurant timings
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Fields to store address
    house = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=6)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be greater than start time.")
    
   

    def __str__(self):
        return self.restaurant_name

    class Meta:
        verbose_name = "restaurant"
        unique_together = ('user', 'GSTIN_num')
        constraints = [
            models.CheckConstraint(check=models.Q(end_time__gt=models.F('start_time')), name='end_time_gt_start_time')
        ]
@receiver(pre_delete, sender=Restaurant)
def delete_file_on_instance_delete(sender, instance, **kwargs):
    # Delete the file if it exists
    if instance.restaurant_image:
        default_storage.delete(instance.restaurant_image.path)
        
# @receiver(pre_save, sender=Restaurant)
# def delete_image_on_field_update(sender, instance,**kwargs):
#     try:
#         # Get the initial instance from the database
#         old_instance = Menu.objects.get(pk=instance.pk)
#         if old_instance.dish_image != instance.restaurant_image :
#             # Delete the old file if it exists
#             if old_instance.restaurant_image:
#                 default_storage.delete(old_instance.restaurant_image.path)
#     except ObjectDoesNotExist:
#         pass
@receiver(pre_save, sender=Restaurant)
def delete_image_on_field_update(sender, instance, **kwargs):
    try:
        # Get the initial instance from the database
        old_instance = Restaurant.objects.get(pk=instance.pk)
        if old_instance.restaurant_image != instance.restaurant_image:
            # Delete the old file if it exists
            if old_instance.restaurant_image:
                default_storage.delete(old_instance.restaurant_image.path)
    except Restaurant.DoesNotExist:
        pass





    
    


# Model for Delivery Agent
class Delivery_Agent(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    rider_name=models.CharField(max_length=100)
    dob=models.DateField()
    age=models.PositiveIntegerField()
    # emp_id=models.CharField(max_length=100,primary_key=True)
    lisence_num=models.CharField(max_length=100,unique=True,null=False,blank=False,primary_key=True)
    area_of_work=models.CharField(max_length=100)
    
    
    def calculate_age(self):
        today=datetime.date.today()
        age=today.year-self.dob.year - ((today.month,today.day)<(self.dob.month,self.dob.day))
        self.age=age
    
    def save(self,*args,**kwargs):
        self.calculate_age()
        super(Delivery_Agent,self).save(*args,**kwargs)
    
    def clean(self):
        if self.age < 18:
            raise ValidationError("Rider must be greater than 18 years")
    
    def __str__(self):
        return self.rider_name
    
    class Meta:
        verbose_name="driver"
        unique_together=('user','lisence_num')
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='rider must be an adult')
        ]
        ordering=('area_of_work',)   
    

    


# Model for Menu
class Menu(models.Model):
    rest_id=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    dish_id=models.CharField(max_length=100)
    veg=models.BooleanField()
    name_of_dish=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    count_per_day=models.IntegerField()
    dish_image=models.ImageField(upload_to="dishImages/",max_length=255,null=True,blank=True,default=None)
    description=models.TextField(max_length=225,null=True,blank=True)
    
    def __str__(self):
        return self.name_of_dish
    
    class Meta:
        verbose_name="dish"
        unique_together=('dish_id','rest_id')
        ordering=('rest_id',)
        constraints = [
            models.UniqueConstraint(fields=['rest_id', 'dish_id'], name='unique_menu_item')
        ]
        
@receiver(pre_delete, sender=Menu)
def delete_file_on_instance_delete(sender, instance, **kwargs):
    # Delete the file if it exists
    if instance.dish_image:
        default_storage.delete(instance.dish_image.path)
        
@receiver(pre_save, sender=Menu)
def delete_image_on_field_update(sender, instance,**kwargs):
    try:
        # Get the initial instance from the database
        old_instance = Menu.objects.get(pk=instance.pk)
        if old_instance.dish_image != instance.dish_image :
            # Delete the old file if it exists
            if old_instance.dish_image:
                default_storage.delete(old_instance.dish_image.path)
    except ObjectDoesNotExist:
        pass
    

        

# Model for Address Book
class Address_Book(models.Model):
    cust_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
    address_type=models.CharField(max_length=100,default=" ")
    flat_no=models.CharField(max_length=100)
    street_address=models.CharField(max_length=255)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pin_code=models.CharField(max_length=6)
    
    def __str__(self):
        return self.cust_id.customer_name
    
    class Meta:
        verbose_name="address"
        ordering=('cust_id__customer_name',)
        unique_together=('cust_id','address_type')
        
    
    