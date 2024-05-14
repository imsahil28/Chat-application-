from django.shortcuts import render
from django.shortcuts import redirect ,render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from chat.models import Profile
from .models import *
from django.core.mail import send_mail
import uuid
from django.conf import settings


def home(request):
    return render(request , 'home.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('login/')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login/')
        
        login(request , user)
        return redirect('user')

    return render(request , 'login.html')

# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Check if the user exists
#         user_obj = User.objects.filter(username=username).first()
#         if user_obj is None:
#             messages.error(request, 'User not found.')
#             return redirect('login')

#         # Check if the profile exists and is verified
#         profile_obj = Profile.objects.filter(user=user_obj).first()
#         if profile_obj is None:
#             messages.error(request, 'Profile not found.')
#             return redirect('login/')
        
#         if not profile_obj.is_verified:
#             messages.error(request, 'Profile is not verified. Check your email.')
#             return redirect('login/')

#         # Authenticate user
#         user = authenticate(username=username, password=password)
#         if user is None:
#             messages.error(request, 'Wrong password.')
#             return redirect('login/')
        
#         # Login user
#         login(request, user)
#         return redirect('user/')

#     return render(request, 'login.html')

   


def register_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('token_send')  

        except Exception as e:
            print(e)

    return render(request, 'register.html')


def token_send(request):
    return render(request , 'token.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        print(profile_obj)
        
        if profile_obj.is_verified:
            messages.success(request, 'Your account is already verified.')
            return redirect('login') 
        else:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('sucess') 

    except Profile.DoesNotExist:
        return redirect('error') 


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        
        if profile_obj is not None:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login') 
            else:
                profile_obj.is_verified = True
                profile_obj.save()
                messages.success(request, 'Your account has been verified.')
                return redirect('success') 
        else:
            # If no profile with the given auth_token exists
            return redirect('error')

    except Exception as e:
        # Handle any other exceptions gracefully
        print(e)
        return redirect('error')

def sucess(request):
    return render(request , 'sucess.html')

def error(request):
    return  render(request , 'error.html')

def generate_auth_token():
    #Your code to generate auth token
     pass

def send_mail_after_registration(email ,auth_token):
    subject = 'Your config needs to be verified'
    message = f'Hi, please click the following link to verify your account: http://127.0.0.1:8000/verify/{auth_token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
    return redirect('/')

def user(request):
    users=Profile.objects.all()
    return render(request,'user.html',{
        'users':users

    })   

from django.shortcuts import get_object_or_404

def room(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    user = profile.user  # No need to fetch user again
    messages = Message.objects.filter(room=profile)

    return render(request, "room.html", {
        "room_name": user.username,  # Pass the username
        "slug": slug,
        "messages": messages
    })