from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.contrib import messages

User=get_user_model()

# Create your views here.
def login_user(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            user=authenticate(email=email,password=password)
            
            if user is None:
                 messages.error(request, "Invalid password")
                 return redirect('/login')
            else :
                 messages.success(request, "Logged in Successfully")
                 login(request,user)
                 return redirect("/register/")
        else:
             messages.error(request, "Invalid email")
        
    return render(request,'login/login.html')

def register_user(request):
    if request.method=="POST":
        email=request.POST.get('email')
        phone_number=request.POST.get('phone')
        password_one=request.POST.get('password_one')
        password_confirm=request.POST.get('password_confirm')
        
        user=User.objects.filter(email=email)
        if user.exists():
            print("user already exists")
            messages.info(request, "Account with this email already exists")
            return redirect('/register/')
        
        if password_one == password_confirm:
            user=User.objects.create(
                email=email,
                phone_number=phone_number
            )
            user.set_password(password_one)
            user.save()
            messages.success(request, "Account Created Successfully")
            return redirect('/login/')
        else :
            messages.info(request, "password does not match")
            print("password does not match")
            
    return render(request,'login/register.html')

def logout_page(request):
    logout(request)
    return('/login/')