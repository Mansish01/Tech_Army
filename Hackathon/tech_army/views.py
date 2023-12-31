from django.shortcuts import render, redirect
from .forms import Signup, LoginForm, UserIDForm, SharedTextareaForm, ReplyForm,DeptloginForm
from .models import Society, UserProfile, SharedTextarea, Reply,Notice,Activity,Municipality1,Municipality2,Municipality3,Municipality4
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
nltk.download('stopwords')
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Activity
from .forms import ActivityForm
stopwords = set(stopwords.words('english'))

with open('tech_army/mnb.pkl', 'rb') as file:
    mnb_model = pickle.load(file)

with open('tech_army/count.pkl', 'rb') as file:
    count_vectorizer = pickle.load(file)

with open('tech_army/tfidf.pkl', 'rb') as file:
    tfidf = pickle.load(file)


def clean_text(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    words = [word for word in text.split(' ') if word not in stopwords]
    words = [stemmer.stem(word) for word in words]
    return " ".join(words)


def detect_hate_speech(text):
    # Preprocess the text and convert it to a bag-of-words representation.
    text_vectorized = count_vectorizer.transform([text])
    text_tfidf = tfidf.transform(text_vectorized)

    # Make predictions using the MNB model.
    prediction = mnb_model.predict(text_tfidf)

    return prediction[0]


def index(request):
    return render(request, 'base.html')


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


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('/logged')
#         return redirect('/logged')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})   
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Check if the user account exists
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user is not None:
                # Authenticate the user
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('/logged')  # Redirect to the logged-in user's dashboard or home page
                else:
                    # Authentication failed, handle the error (e.g., show an error message)
                    pass
            else:
                # User account does not exist, handle the error (e.g., show an error message)
                pass
        else:
            # Form is not valid, handle the error (e.g., show an error message)
            pass
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def login_view_dept(request):
    if request.method == 'POST':
        form = DeptloginForm(request.POST)
        if form.is_valid():
           
            return redirect('/logged1')  # Redirect to the desired URL after successful login
           
    else:
        form = DeptloginForm()

    return render(request, 'deptlogin.html', {'form': form })

def logged1(request):
    
    return render(request, 'logged1.html',)        
        
        
        
        
@login_required
def logged(request):
    products = Society.objects.all()
    params = {'product': products}
    return render(request, 'logged.html', params)


@login_required
def update_user_id(request):
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        form = UserIDForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('/update_user_id')
    else:
        form = UserIDForm(instance=user_profile)

    return render(request, 'studentid.html', {'form': form, 'user_profile': user_profile})


def shared_textarea(request,municipality_name):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        

        if user_profile.municipality_name == municipality_name :
    
            form = SharedTextareaForm()
            entries = SharedTextarea.objects.all()
            user_profiles = UserProfile.objects.all()
            params = {'user_profiles': user_profiles}

            if request.method == 'POST':
                form = SharedTextareaForm(request.POST)
                if form.is_valid():
                    content = form.cleaned_data['content']
                    title = form.cleaned_data['title']
                    # Perform hate speech detection using the MNB model.
                    text_clean = clean_text(content)  # Preprocess the text and get a list of words.
                    print(text_clean)
                    hate_speech_prediction = detect_hate_speech(text_clean)
                    print(hate_speech_prediction)

                    if hate_speech_prediction == 1:
                        return redirect('/logged')  # Make sure you have an 'index' view to handle this redirection.
                        # Handle hate speech (e.g., display an error message or take appropriate action).
                        # You may want to show an error message here.

                    shared_textarea = SharedTextarea.objects.create(content=content, title=title, user=request.user)
                    shared_textarea.user_profile = UserProfile.objects.get(user=request.user)
                    shared_textarea.save()
                    return redirect('/shared_textareasdep')
        
            return render(request, 'shared_textarea.html', {'form': form, 'entries': entries, 'params': params, 'username': request.user.username})
   
        else:
            return redirect('/shared_textareasdep')
            
        
    except UserProfile.DoesNotExist:
       pass
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
            shared_textarea = Reply.objects.create(content=content, title=title, user=request.user)
            shared_textarea.user_profile = UserProfile.objects.get(user=request.user)
            shared_textarea.save()
            return redirect('/reply_textarea')

    return render(request, 'reply_textarea.html', {'form': form, 'entries': entries, 'params': params, 'username': request.user.username})
def showsolnonly(request):
    form = ReplyForm()
    entries = Reply.objects.all()
    user_profiles = UserProfile.objects.all()
    params = {'user_profiles': user_profiles}

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            title = form.cleaned_data['title']
            shared_textarea = Reply.objects.create(content=content, title=title, user=request.user)
            shared_textarea.user_profile = UserProfile.objects.get(user=request.user)
            shared_textarea.save()
            return redirect('/reply_textarea')

    return render(request, 'viewsoln.html', {'form': form, 'entries': entries, 'params': params, 'username': request.user.username})



def Noticeboard(request):
    product1 = Notice.objects.all()
    params1 = {'product1': product1}
    product2 = Activity.objects.all()
    params2 = {'product2': product2}
    context = {**params1, **params2}
    return render(request, 'base.html', context)


def emergency(request):
    
      return render(request, 'emergency.html')




def shared_textareas(request):
    
            form = SharedTextareaForm()
            entries = SharedTextarea.objects.all()
            user_profiles = UserProfile.objects.all()
            params = {'user_profiles': user_profiles}

            if request.method == 'POST':
                form = SharedTextareaForm(request.POST)
                if form.is_valid():
                    content = form.cleaned_data['content']
                    title = form.cleaned_data['title']
                    # Perform hate speech detection using the MNB model.
                    text_clean = clean_text(content)  # Preprocess the text and get a list of words.
                    print(text_clean)
                    hate_speech_prediction = detect_hate_speech(text_clean)
                    print(hate_speech_prediction)

                    if hate_speech_prediction == 1:
                        return redirect('/warning')  # Make sure you have an 'index' view to handle this redirection.
                        # Handle hate speech (e.g., display an error message or take appropriate action).
                        # You may want to show an error message here.

                    shared_textarea = SharedTextarea.objects.create(content=content, title=title, user=request.user)
                    shared_textarea.user_profile = UserProfile.objects.get(user=request.user)
                    shared_textarea.save()
                    return redirect('/shared_textareas')
        
            return render(request, 'shared_textarea.html', {'form': form, 'entries': entries, 'params': params, 'username': request.user.username})
   
def shared_textareasdep(request):
    
            form = SharedTextareaForm()
            entries = SharedTextarea.objects.all()
            user_profiles = UserProfile.objects.all()
            params = {'user_profiles': user_profiles}

            if request.method == 'POST':
                form = SharedTextareaForm(request.POST)
                if form.is_valid():
                    content = form.cleaned_data['content']
                    title = form.cleaned_data['title']
                    # Perform hate speech detection using the MNB model.
                    text_clean = clean_text(content)  # Preprocess the text and get a list of words.
                    print(text_clean)
                    hate_speech_prediction = detect_hate_speech(text_clean)
                    print(hate_speech_prediction)

                    if hate_speech_prediction == 1:
                        return redirect('/logged')  # Make sure you have an 'index' view to handle this redirection.
                        # Handle hate speech (e.g., display an error message or take appropriate action).
                        # You may want to show an error message here.

                    shared_textarea = SharedTextarea.objects.create(content=content, title=title, user=request.user)
                    shared_textarea.user_profile = UserProfile.objects.get(user=request.user)
                    shared_textarea.save()
                    return redirect('/shared_textareasdep')
        
            return render(request, 'logged2.html', {'form': form, 'entries': entries, 'params': params, 'username': request.user.username})
def update_activity(request):
    activity = Activity.objects.first()  # Assuming you want to update the first activity instance, modify this based on your requirement

    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activity_detail')  # Redirect to the appropriate view after form submission
    else:
        form = ActivityForm(instance=activity)

    return render(request, 'update_activity.html', {'form': form})
def municipality1(request):
    products = Municipality1.objects.all()
    params = {'product': products}
    return render(request, 'mun1.html', params)
    
    
    
    
def municipality2(request):
    products = Municipality2.objects.all()
    params = {'product': products}
    return render(request, 'mun2.html', params)
    
    
    
    
def municipality3(request):
    products = Municipality3.objects.all()
    params = {'product': products}
    return render(request, 'mun3.html', params)
    
    
    
    
def municipality4(request):
    products = Municipality4.objects.all()
    params = {'product': products}
    return render(request, 'mun4.html', params)
    
def warning(request) :
      
     return render(request, 'warning.html')
