from django.shortcuts import render,redirect
from . forms import Signup
from .models import Society,UserProfile
from django.db import IntegrityError

def index(request):
    return render(request,'index.html')
def signup(request):
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                user_profile = UserProfile.objects.create(user=user)
            except IntegrityError:
                # StudentProfile already exists for the user, handle the error
                # e.g., display an error message or redirect to a different page
                pass
            return redirect('/login')  
    else:
        form = Signup()

    return render(request, 'signup.html', {'form': form})
