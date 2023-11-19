from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.contrib import messages
from main.models import *
import uuid
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q

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
                    return redirect("/user-home/")
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
                if Restaurant.objects.filter(user=user):
                    messages.success(request, "Logged in Successfully")
                    login(request,user)
                    return redirect("/restaurant-home/")
                else:
                    messages.error(request, "User not registered as restaurant")
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
                if Delivery_Agent.objects.filter(user=user):
                    messages.success(request, "Logged in Successfully")
                    login(request,user)
                    return redirect("/register-rider/")
                else:
                    messages.error(request, "User not registered as rider")
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
        try:
            restaurant_image=request.FILES.get('image')
        except :
            pass
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
                restaurant_image=restaurant_image,
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

def logout_restaurant(request):
    logout(request)
    return redirect('/login-restaurant/')

def logout_user(request):
    logout(request)
    return redirect('/login-user/')

def logout_rider(request):
    logout(request)
    return redirect('/login-rider/')

@login_required(login_url='/login-restaurant/')
def restaurant_home(request):
    if request.user is not None:
        restaurant=Restaurant.objects.get(user=request.user)
        context={
            "restaurant":restaurant
        }
        return render(request, 'restaurant/RestHomepage.html',context)
    else:
        return HttpResponse("Error Occured. Please try again.")
     
        
@login_required(login_url='/login-restaurant/')
def restaurant_display_menu(request):
    if request.user is not None:
        restaurant=Restaurant.objects.get(user=request.user)
        menu=Menu.objects.filter(rest_id=restaurant)
        context={
            "restaurant":restaurant,
            "menu":menu,
        }
        return render(request,'restaurant/DisplayMenu.html',context)
    else:
        return HttpResponse("Error Occured. Please try again.")
   
    
@login_required(login_url='/login-restaurant/')
def restaurant_addTo_menu(request):
    if request.user is not None:
        if request.method=='POST':
            veg=request.POST.get('isveg')
            name_of_dish=request.POST.get('name')
            description=request.POST.get('desc')
            price=request.POST.get('price')
            count_per_day=request.POST.get('count')
            try:
                dish_image=request.FILES.get('image')
            except :
                pass
            
            if veg=="on":
                veg=True
            else:
                veg=False
            
            dish_id= "DISH" + str(uuid.uuid4().hex)[:3]
            restaurant=Restaurant.objects.get(user=request.user)
            dish=Menu.objects.create(
                rest_id=restaurant,
                dish_id=dish_id,
                veg=veg,
                name_of_dish=name_of_dish,
                description=description,
                price=price,
                count_per_day=count_per_day,
                dish_image=dish_image
            )
            dish.save()
            messages.success(request, "Dish Added Successfully")
            return redirect('/restaurant-menu/')
        
        return render(request,'restaurant/Addmenu.html')
            
    else:
        return HttpResponse("Error Occured. Please try again.") 
            
        
@login_required(login_url='/login-restaurant/')   
def restaurant_profile(request):
    if request.user is not None:
        restaurant=Restaurant.objects.get(user=request.user)
        return render(request,'restaurant/rest-profile.html',{"restaurant":restaurant})
    else:
        return HttpResponse("Error Occured. Please try again.") 
        
@login_required(login_url='/login-restaurant/')
def restaurant_edit_profile(request):
    if request.user is not None:
        restaurant=Restaurant.objects.get(user=request.user)
        user=User.objects.get(email=request.user)
        if request.method=="POST":
            if request.POST.get('email'):
                user.email=request.POST.get('email')
                user.save()
            if request.POST.get('phone'):
                user.phone_number=request.POST.get('phone')
                user.save()
            if request.POST.get('name'):
                restaurant.retaurant_name=request.POST.get('name')
            if request.POST.get('stime'):
                restaurant.start_time=request.POST.get('stime')
            if request.POST.get('etime'):
                restaurant.end_time=request.POST.get('etime')
            if request.POST.get('gstin'):
                restaurant.GSTIN_num=request.POST.get('gstin')
            if request.POST.get('house'):
                restaurant.house=request.POST.get('house')
            if request.POST.get('street'):
                restaurant.street_address=request.POST.get('street')
            if request.POST.get('city'):
                restaurant.city=request.POST.get('city')
            if request.POST.get('state'):
                restaurant.state=request.POST.get('state')
            if request.POST.get('pincode'):
                restaurant.pin_code=request.POST.get('pincode')
            if request.FILES.get('image'):
                restaurant.restaurant_image=request.FILES.get('image')
            restaurant.save()
            messages.success(request, "Changes made successfully")
            return redirect('/restaurant-profile/')
        return render(request,'restaurant/edit-restaurant.html')
    else:
        return HttpResponse("Error Occured.")
    
@login_required(login_url='/login-restaurant/')
def restaurant_change_password(request):
    if request.user is not None:
        user=User.objects.get(email=request.user)
        if request.method=="POST":
            new=request.POST.get("new")
            confirm=request.POST.get('confirm')
            if new ==confirm:
                user.set_password(new)
                user.save()
                return redirect('/login-restaurant/')
            else:
                messages.error(request, "Password do not match. Try again")
                return redirect('/restaurant-change-password/')
        return render(request,'restaurant/change-password.html')
    else:
        return HttpResponse("Error Occured.")
    
 
 
@login_required(login_url='/login-restaurant/')
def restaurant_edit_dish(request,dishId):
    if request.user is not None:
        dish=Menu.objects.get(dish_id=dishId)   
        if request.method=="POST":
            if request.POST.get('isveg'):
                veg=request.POST.get('isveg')
                if veg=="on":
                    veg=True
                else:
                    veg=False 
                dish.veg=veg 
            if request.POST.get('name'):
                dish.name_of_dish=request.POST.get('name')
            if request.POST.get('desc'):
                dish.description=request.POST.get('desc')
            if request.POST.get('price'):
                dish.price=request.POST.get('price')
            if request.POST.get('count'):
                dish.count_per_day=request.POST.get('count')
            try:
                if request.POST.get('image'):
                    dish.dish_image=request.FILES.get('image')
            except :
                pass
            dish.save()
            return redirect('/restaurant-menu/')
        return render(request,'restaurant/edit-menu.html',{"dish":dish})
    else:
        return HttpResponse("Error Occured.")
    
@login_required(login_url='/login-restaurant/')
def restaurant_delete_dish(request,dishId):
    dish=Menu.objects.get(dish_id=dishId)
    dish.delete()
    return redirect('/restaurant-menu/')
            
            
 #customer 
@login_required(login_url='/login-user/')               
def customer_home(request):
    if request.user is not None:
        restaurants=Restaurant.objects.all()[0:100]
        
        
        if request.GET.get('search'):
            search=request.GET.get('search')
            rest_all=Restaurant.objects.all()
            all_dishes=Menu.objects.all()
            query1=rest_all.filter(
                Q(restaurant_name__icontains=search)
            )
            query2=all_dishes.filter(
                Q(name_of_dish__icontains=search)|
                Q(description__icontains=search)     
            )
            restaurant_ids_query1 = query1.values_list('GSTIN_num', flat=True)
            restaurant_ids_query2 = query2.values_list('rest_id', flat=True)
            unique_restaurant_ids = set(restaurant_ids_query1) | set(restaurant_ids_query2)
            restaurants = rest_all.filter(GSTIN_num__in=unique_restaurant_ids)
            print(restaurants)
            # return redirect('/user-home#restaurants-to-explore')
            # return HttpResponseRedirect('/user-home#restaurants-to-explore', {"restaurants":restaurants})
            
            
    return render(request,'customers/cust-homepage.html',{"restaurants":restaurants})


@login_required(login_url='/login-user/')                 
def customer_profile(request):
    if request.user is not None:
        customer=Customer.objects.get(user=request.user)
        return render(request,'customers/cust-profile.html',{"customer":customer})
    else:
        return HttpResponse("Error Occured. Please try again.") 
    

@login_required(login_url='/login-user/')                     
def customer_profile_edit(request):
    if request.user is not None:
        customer=Customer.objects.get(user=request.user)
        user=User.objects.get(email=request.user)
        if request.method=="POST":
            if request.POST.get('email'):
                user.email=request.POST.get('email')
                user.save()
            if request.POST.get('phone'):
                user.phone_number=request.POST.get('phone')
                user.save()
            if request.POST.get('name'):
                customer.customer_name=request.POST.get('name')
            if request.POST.get('dob'):
                customer.dob=request.POST.get('dob')
            customer.save()
            messages.success(request, "Changes made successfully")
            return redirect('/user-profile/')
        return render(request,'customers/cust-edit-profile.html')
    else:
        return HttpResponse("Error Occured.")
    
    
@login_required(login_url='/login-user/')                     
def customer_change_password(request):
    if request.user is not None:
        user=User.objects.get(email=request.user)
        if request.method=="POST":
            new=request.POST.get("new")
            confirm=request.POST.get('confirm')
            if new ==confirm:
                user.set_password(new)
                user.save()
                return redirect('/login-user/')
            else:
                messages.error(request, "Password do not match. Try again")
                return redirect('/user-change-password/')
        return render(request,'customers/cust-change-password.html')
    else:
        return HttpResponse("Error Occured.")
    


@login_required(login_url='/login-user/')                     
def customer_add_address(request):
    if request.user is not None:
        if request.method=="POST":
            cust_id=Customer.objects.get(user=request.user)
            address_type=""
            if request.POST.get('home'):
                address_type="Home"
            if request.POST.get('work'):
                address_type="Work"
            if request.POST.get('hotel'):
                address_type="Hotel"
            if request.POST.get('other'):
                address_type="Other"
            if Address_Book.objects.filter(cust_id=cust_id,address_type=address_type):
                messages.error(request, "Address of this type Already exists.")
                return redirect('/user-add-address/')
            flat_no=request.POST.get('flat_no')            
            street_address=request.POST.get('street')            
            city=request.POST.get('city')            
            state=request.POST.get('state')            
            pin_code=request.POST.get('pincode') 
            
            address=Address_Book.objects.create(
                cust_id=cust_id,
                address_type=address_type,
                flat_no=flat_no,
                street_address=street_address,
                city=city,
                state=state,
                pin_code=pin_code
            )
            address.save()
            messages.success(request, "Address added successfully")
            return redirect('/user-profile/')

        return render(request,'customers/add-address.html')   
    else:
        return HttpResponse("Error Occured.")        
