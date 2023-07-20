from django.shortcuts import render,redirect
from . forms import Signup,LoginForm,UserIDForm
from .models import Society,UserProfile,SharedTextarea,Reply
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SharedTextareaForm,ReplyForm

def index(request):
    return render(request,'base.html')
def signup(request):
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                user_profile = UserProfile.objects.create(user=user)
            except IntegrityError:
                
                pass
            return redirect('/login')  
    else:
        form = Signup()

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('/logged')  
        return redirect('/logged')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
    
@login_required
def logged(request):
    products = Society.objects.all()
    params ={'product':products}

    return render(request,'logged.html',params)
@login_required
def update_user_id(request):
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        
        user_profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        form = UserIDForm(request.POST,request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('/update_user_id')
    else:
        form = UserIDForm(instance=user_profile)

    return render(request, 'studentid.html', {'form': form, 'user_profile': user_profile})   


def shared_textarea(request):
    form = SharedTextareaForm()
    entries = SharedTextarea.objects.all()
    user_profiles = UserProfile.objects.all()
    params = {'user_profiles': user_profiles}
    
    if request.method == 'POST':
        form = SharedTextareaForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            title = form.cleaned_data['title']
            shared_textarea = SharedTextarea.objects.create(content=content,title=title, user=request.user)
            shared_textarea.user_profile = UserProfile.objects.get(user=request.user)
            shared_textarea.save()
            return redirect('/shared_textarea')
    
    return render(request, 'shared_textarea.html', {'form': form, 'entries': entries, 'params': params, 'username': request.user.username})

def ReplyForms(request):
    form = ReplyForm()
    entries = Reply.objects.all()
    user_profiles = UserProfile.objects.all()
    params = {'user_profiles': user_profiles}
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            title = form.cleaned_data['title']
            shared_textarea = Reply.objects.create(content=content,title=title, user=request.user)
            shared_textarea.user_profile = UserProfile.objects.get(user=request.user)
            shared_textarea.save()
            return redirect('/reply_textarea')
    
    return render(request, 'reply_textarea.html', {'form': form, 'entries': entries, 'params': params, 'username': request.user.username})