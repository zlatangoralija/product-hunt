from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(username = request.POST['username'], password=request.POST['password'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Password has to bee confirmed'})
    else:
        return render(request, 'accounts/signup.html')

def login(request):
     if request.method == 'POST':
         user = auth.authenticate(username = request.POST['username'], password = request.POST['password'])
         if user is not None:
             auth.login(request, user)
             return redirect('home')
         else:
             return render(request, 'accounts/login.html', {'error': 'Username or password is not correct'})
     else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')
