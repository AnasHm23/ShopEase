from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from .forms import RegisterForm

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
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Registration successful. you are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. please correct the errors below.')
    else:
        form =  RegisterForm()
    return render(request, 'home.html', {'form': form})
