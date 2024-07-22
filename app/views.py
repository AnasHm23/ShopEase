from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages


# Create your views here.
def home(request):
    context = {}
    # check if the user logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, 'Login failed please try again.')
            return redirect('home')
    else:
        return render(request, 'home.html', {'context': context})

def logout_user(request):
    logout(request)
    messages.success(request, "You've been Logged out.")
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
    user = username