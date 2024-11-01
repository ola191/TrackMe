from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'last_login', 'is_superuser', 'username', 'first_name',
            'last_name', 'email', 'is_staff', 'is_active', 'date_joined',
            'bio', 'profile_picture', 'status'
        ]
        widgets = {
            'id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'last_login': forms.TextInput(attrs={'readonly': 'readonly'}),
            'date_joined': forms.TextInput(attrs={'readonly': 'readonly'}),
            'is_superuser': forms.TextInput(attrs={'readonly': 'readonly'}),
            'is_staff': forms.TextInput(attrs={'readonly': 'readonly'}),
            'is_active': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
