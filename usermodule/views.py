from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Users
from adminmodule.models import Hotel,HotelPayment
from django.contrib.auth import authenticate, login as lg
import random

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        gender = request.POST['gender']
        mobile = request.POST['phone']
        image = request.FILES.get('image')
        print(image)

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password1, first_name=first_name,
                                         last_name=last_name, email=email)
        user.save()

        otp = ''.join([str(random.randint(10000, 99999)) ])
        user_profile = Users.objects.create(user_id=user, gender=gender, image=image, mobile=mobile, otp=otp)
        user_profile.save()

        send_mail(
            'Your OTP for Login',
            f'Your OTP is: {otp}',
            'vsv8639243604@gmail.com',
            [email],
            fail_silently=False,
        )

        messages.info(request, 'An OTP has been sent to your email. Please check and enter the OTP.')
        return redirect('email_verification')

    return render(request, 'signup.html')


def email_verification(request):
    if request.method == "POST":
        otp_entered = request.POST.get('otp')

        if Users.objects.filter(otp=otp_entered).exists():
            messages.info(request, 'Email verification successful. Please proceed to login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('email_verification')

    return render(request, 'email_verification.html')
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Users.objects.filter(user_id__username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                if len(username) == 4:
                    lg(request, user)
                    messages.success(request, 'Login successful. Welcome, admin!')
                    return redirect('adminhomepage')
                else:
                    lg(request, user)
                    messages.success(request, 'Login successful. Welcome!')
                    return redirect('userhomepage')
            else:
                messages.error(request, 'Invalid Credentials')
                return render(request, 'login.html', {'fail': True})
        else:
            messages.error(request, 'Invalid OTP')
            return render(request, 'login.html', {'fail': True})
    else:
        return render(request, 'login.html', {'fail': False})

def logout(request):
    return render(request,'home.html')

def userhomepage(request):
    return render(request,'userhomepage.html')

def bookhotel(request):
    hotels = Hotel.objects.all()
    return render(request,'bookhotel.html',{'hotels': hotels})

def contactus(request):
    return render(request,'contactus.html')

def viewprofile(request):
    profile = request.user.users
    return render(request,'view_profile.html',{'profile':profile})


def viewstatus(request):
    payments = HotelPayment.objects.filter(paid=True)
    payment_data = []
    for payment in payments:
        amount_paid = int(payment.amount) / 100
        payment_info = {
            'hotel_name': payment.name,
            'amount_paid': amount_paid,
            'order_id': payment.order_id
        }
        payment_data.append(payment_info)
    return render(request, 'viewstatus.html', {'payments': payment_data})