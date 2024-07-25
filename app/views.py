from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import User
#email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.urls import reverse, reverse_lazy
from .tokens import account_activation_token
# password reset
from django.contrib.auth import views as auth_views


# AUTHENTICATION VIEWS
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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your ShopEase account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'home.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been confirmed.')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')


# PASSWORD RESET
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'home.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Password reset email has been sent.')
        return self.render_to_response(self.get_context_data(form=form))

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'home.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your password has been reset successfully. You can log in with the new password.')
        return self.render_to_response(self.get_context_data(form=form))
