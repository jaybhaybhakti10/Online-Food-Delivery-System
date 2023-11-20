from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from main.models import *
from order.models import *
import uuid
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q

User=get_user_model()

@login_required(login_url='/login-user/')
def customer_add_to_cart(request,dish_id,rest_id):
    if request.user is not None:
        cust_id=Customer.objects.get(user=request.user)
        item=Menu.objects.get(dish_id=dish_id)
        cart_item=Cart.objects.filter(cust_id=cust_id,item=item)
        if cart_item:
            cart_item[0].item_count +=1
            cart_item[0].amount=cart_item[0].item_count * item.price
            cart_item[0].save()
            return redirect('/view-cart/')
        else:
            cart_item=Cart.objects.create(
                cust_id=cust_id,
                item_count=1,
                amount=item.price,
                item=item,
            )
            cart_item.save()
            return redirect('/view-cart/')
        
    # cust_id=Customer.objects.get(user=request.user).cust_id
    # cart_user=Cart.objects.filter(cust_id=cust_id)
    
    # return render(request,'customers/view-cart.html',{"cart":cart_user})
    restaurant=Restaurant.objects.get(GSTIN_num=rest_id)
    menu=Menu.objects.filter(rest_id=restaurant)
    context={
        "restaurant":restaurant,
        "menu":menu
    }
    return render(request,'customers/menu-page.html',context)

@login_required(login_url='/login-user/')
def customer_view_cart(request):
    cust_id=Customer.objects.get(user=request.user).cust_id
    cart_user=Cart.objects.filter(cust_id=cust_id)
    sub_total=0
    total=0
    for item in cart_user:
        sub_total+=item.amount
    gst=0.18*float(sub_total)
    delivery_fee=80
    total=gst + float(sub_total)+delivery_fee
    
    return render(request,'customers/cart.html',{"cart":cart_user,"sub_total":sub_total,"delivery_fee":delivery_fee,"gst":gst,"total":total})