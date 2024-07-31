from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .models import EmailAddress


# Override UserCreationForm
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

# Override SetPasswordForm
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].error_messages = {
            'required': 'Please enter a new password.',
            'invalid': '',
        }
        self.fields['new_password2'].error_messages = {
            'required': 'Please confirm your new password.',
            'invalid': '',
        }

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

class EmailAddresForm(forms.ModelForm):
    class Meta:
        model = EmailAddress
        fields = ['email', 'is_active']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_active = self.cleaned_data.get('is_active', False)

        if is_active and EmailAddress.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("active email addresses must be unique.")
    
        return email