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
from django.db.models import Q,Count
from random import randint

User=get_user_model()

@login_required(login_url='/login-user/')
def customer_add_to_cart(request,dish_id,rest_id):
    if request.user is not None:
        cust_id=Customer.objects.get(user=request.user)
        item=Menu.objects.get(dish_id=dish_id)
        cart_item=Cart.objects.filter(cust_id=cust_id,item=item,status="IN_CART")
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
    cart_user=Cart.objects.filter(cust_id=cust_id,status="IN_CART")
    sub_total=0
    total=0
    for item in cart_user:
        sub_total+=item.amount
    gst=0.18*float(sub_total)
    delivery_fee=80
    total=gst + float(sub_total)+delivery_fee
    
    return render(request,'customers/cart.html',{"cart":cart_user,"sub_total":sub_total,"delivery_fee":delivery_fee,"gst":gst,"total":total})

@login_required(login_url='/login-user/')
def delete_item_from_cart(request,id):
    cust_id=Customer.objects.get(user=request.user).cust_id
    cart_item=Cart.objects.get(cust_id=cust_id,id=id)
    print(cart_item)
    if cart_item.item_count==1:
        cart_item.delete()
        return redirect('/view-cart/')
    elif cart_item.item_count>1:
        cart_item.item_count-=1
        cart_item.save()
        print(cart_item.item_count)
        return redirect('/view-cart/')
    
@login_required(login_url='/login-user/')
def place_order(request):
    customer=Customer.objects.get(user=request.user)
    address=Address_Book.objects.filter(cust_id=customer.cust_id)
    cart_user=Cart.objects.filter(cust_id=customer.cust_id,status="IN_CART")
    sub_total=0
    total=0
    total_count=0
    for item in cart_user:
        sub_total+=item.amount
        total_count+=item.item_count
    total=0.18*float(sub_total) + float(sub_total)+80
    context={
        "addresses":address,
        "cart":cart_user,
        "total":total,
        "total_count":total_count
    }
    if request.method=="POST":
        if request.POST.get('Home'):
            address=address.get(address_type="Home")
        if request.POST.get('Work'):
            address=address.get(address_type="Work")
        if request.POST.get('Hotel'):
            address=address.get(address_type="Hotel")
        if request.POST.get('Other'):
            address=address.get(address_type="Other")
            
        if request.POST.get('credit'):
            payment="credit"
        if request.POST.get('debit'):
            payment="debit"
        if request.POST.get('cash'):
            payment="cash"
        
        # create order object
        rest_id=cart_user[0].item.rest_id
        cust_id=customer
        
        number_of_riders=Delivery_Agent.objects.filter(area_of_work=address.city)
        print(number_of_riders.count())
        random_integer=randint(0,number_of_riders.count()-1)
        rider_id=Delivery_Agent.objects.filter(area_of_work=address.city)[random_integer]
    
        order_id="ODR" + str(uuid.uuid4().hex)[:3]
        
        order=Order.objects.create(
            order_id=order_id,
            rest_id=rest_id,
            cust_id=cust_id,
            rider_id=rider_id,
            address_of_delivery=address,
            total_amount=total,
            status_of_delivery="ORDERED"
        )
        # as many to many relation
        for item in cart_user:
            order.cart_item.add(item)
        order.save()
        # changing status of cart items to ordered
        for item in cart_user:
            item.status="ORDERED"
            item.save()
            # saving payment details if cash
        if payment=="cash":
            current_datetime = datetime.now()
            pay=Payment.objects.create(
            order_id=order,
            payment_method="cash",
            payment_status="PAID",
            payment_date=current_datetime.strftime("%Y-%m-%d"),
            payment_time=current_datetime.strftime("%H:%M:%S"),
            transaction_id="TRSC"+ str(uuid.uuid4().hex)[:3]
            
            )
            pay.save()
            
        return redirect('/payment/'+payment+"/"+str(order.order_id))
        
    return render(request,'customers/place-order.html',context)


@login_required(login_url='/login-user/')
def order_payment(request,method,order_id):
    if request.method=="POST":
        order_id=Order.objects.get(order_id=order_id)
        current_datetime = datetime.now()
        payment_date = current_datetime.strftime("%Y-%m-%d")
        payment_time= current_datetime.strftime("%H:%M:%S")
        transaction_id="TRSC"+ str(uuid.uuid4().hex)[:3]
        
        payment=Payment.objects.create(
            order_id=order_id,
            payment_method=method,
            payment_status="PAID",
            payment_date=payment_date,
            payment_time=payment_time,
            transaction_id=transaction_id
            
        )
        payment.save()
        return redirect('/user-orders/')
    customer=Customer.objects.get(user=request.user)
    order=Order.objects.get(cust_id=customer.cust_id,status_of_delivery="ORDERED")
    return render(request,'customers/payment.html',{"order":order})

@login_required(login_url='/login-user/')
def view_order(request):
    customer=Customer.objects.get(user=request.user)
    current_order=Order.objects.filter(cust_id=customer.cust_id,status_of_delivery="ORDERED")
    past_orders=Order.objects.filter(cust_id=customer.cust_id,status_of_delivery="DELIVERED")
    current_items=Cart.objects.filter(cust_id=customer.cust_id,status="ORDERED")
    return render(request,'customers/order-view.html',{"current_order":current_order,"past_orders":past_orders,"current_items":current_items})