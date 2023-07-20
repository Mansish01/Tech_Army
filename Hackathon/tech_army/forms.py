from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile



class Signup(UserCreationForm):
   
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
    
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
class UserIDForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user','citizenship_id','municipality_name','ward_no','image')

    user = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your student ID',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    citizenship_id = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your student ID',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    municipality_name= forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your student ID',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    ward_no = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your student ID',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
class SharedTextareaForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    title = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 10}))
class ReplyForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    title = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 10}))