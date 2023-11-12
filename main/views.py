from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.contrib import messages
from main.models import *
from django.db.models import Count
import uuid
from datetime import datetime

User=get_user_model()

# Create your views here.
def home(request):
    return render(request,'login/home.html')


def login_user(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            user=authenticate(email=email,password=password)
            
            if user is None:
                messages.error(request, "Invalid password")
                return redirect('/login-user')
                
            else :
                if Customer.objects.filter(user=user):
                    messages.success(request, "Logged in Successfully")
                    login(request,user)
                    return redirect("/register-user/")
                else:
                    messages.error(request, "User not registered as customer")
        else:
             messages.error(request, "Invalid email")
        
    return render(request,'login/login-user.html')

def login_restaurant(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            user=authenticate(email=email,password=password)
            
            if user is None:
                 messages.error(request, "Invalid password")
                 return redirect('/login-resatuarant')
            else :
                 messages.success(request, "Logged in Successfully")
                 login(request,user)
                 return redirect("/register-restaurant/")
        else:
             messages.error(request, "Invalid email")
        
    return render(request,'login/login-rest.html')

def login_rider(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            user=authenticate(email=email,password=password)
            
            if user is None:
                 messages.error(request, "Invalid password")
                 return redirect('/login-rider')
            else :
                 messages.success(request, "Logged in Successfully")
                 login(request,user)
                 return redirect("/register-rider/")
        else:
             messages.error(request, "Invalid email")
        
    return render(request,'login/login-rider.html')

def register_user(request):
    if request.method=="POST":
        email=request.POST.get('email')
        phone_number=request.POST.get('phone')
        password_one=request.POST.get('password_one')
        password_confirm=request.POST.get('password_confirm')
        customer_name=request.POST.get('name')
        dob=request.POST.get('date')
        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        
        user=User.objects.filter(email=email)
        if user.exists():
            print("user already exists")
            messages.info(request, "Account with this email already exists")
            return redirect('/register-user/')
        
        if password_one == password_confirm:
            user=User.objects.create(
                email=email,
                phone_number=phone_number
            )
            user.set_password(password_one)
            user.save()
            
            cust_id = "CUST" + str(uuid.uuid4().hex)[:5]
            
            cust=Customer.objects.create(
                user=user,
                customer_name=customer_name,
                dob=dob_date,
                cust_id=cust_id
            )
            
            cust.save()
            
            messages.success(request, "Account Created Successfully")
            return redirect('/login-user/')
        else :
            messages.info(request, "password does not match")
            print("password does not match")
            
    return render(request,'login/register-user.html')

def register_restaurant(request):
    if request.method=="POST":
        email=request.POST.get('email')
        phone_number=request.POST.get('phone')
        password_one=request.POST.get('password_one')
        password_confirm=request.POST.get('password_confirm')
        restaurant_name=request.POST.get('name')
        start_time=request.POST.get('stime')
        end_time=request.POST.get('etime')
        gstin=request.POST.get('gstin')
        house=request.POST.get('house')
        street_address=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        
        user=User.objects.filter(email=email)
        if user.exists():
            print("user already exists")
            messages.info(request, "Account with this email already exists")
            return redirect('/register-restaurant/')
        
        if password_one == password_confirm:
            user=User.objects.create(
                email=email,
                phone_number=phone_number
            )
            user.set_password(password_one)
            user.save()
            
            
            rest=Restaurant.objects.create(
                user=user,
                restaurant_name=restaurant_name,
                GSTIN_num=gstin,
                start_time=start_time,
                end_time=end_time,
                house=house,
                street_address=street_address,
                city=city,
                state=state,
                pin_code=pincode,
                
                
            )
            
            rest.save()
            
            messages.success(request, "Account Created Successfully")
            return redirect('/login-restaurant/')
        else :
            messages.info(request, "password does not match")
            print("password does not match")
            
    return render(request,'login/register-rest.html')

def register_rider(request):
    if request.method=="POST":
        email=request.POST.get('email')
        phone_number=request.POST.get('phone')
        password_one=request.POST.get('password_one')
        password_confirm=request.POST.get('password_confirm')
        rider_name=request.POST.get('name')
        dob=request.POST.get('date')
        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        license_num=request.POST.get('license')
        area_of_work=request.POST.get('area')
        
        user=User.objects.filter(email=email)
        if user.exists():
            print("user already exists")
            messages.info(request, "Account with this email already exists")
            return redirect('/register-rider/')
        
        if password_one == password_confirm:
            user=User.objects.create(
                email=email,
                phone_number=phone_number
            )
            user.set_password(password_one)
            user.save()
            
            
            rider=Delivery_Agent.objects.create(
                user=user,
                rider_name=rider_name,
                dob=dob_date,
                lisence_num=license_num,
                area_of_work =area_of_work
            )
            
            rider.save()
            
            messages.success(request, "Account Created Successfully")
            return redirect('/login-rider/')
        else :
            messages.info(request, "password does not match")
            print("password does not match")
            
    return render(request,'login/register-rider.html')

def logout_page(request):
    logout(request)
    return('/login/')