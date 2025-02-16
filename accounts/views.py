from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CustomUser


def home(request):
    return render(request, 'accounts/home.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import CustomUser

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import CustomUser

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken!")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered!")
            return redirect('register')

        user = CustomUser.objects.create_user(
            username=username, email=email, password=password1,
            first_name=first_name, last_name=last_name
        )
        login(request, user)
        return redirect('core:dashboard')

    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, "Грешно потребителско име или парола!")
            return redirect('login')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')
