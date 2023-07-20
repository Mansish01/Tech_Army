
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name='tech_army'
urlpatterns = [
    
path('', views.Noticeboard,name='index1'),
path('index', views.Noticeboard,name='index'),
path('signup', views.signup, name='signup'),
path('login', views.login_view, name='login'),
path('logged', views.logged, name='logged'),
path('logged1', views.logged1, name='logged1'),
path('profile/', views.update_user_id, name='profile'),
path('update_user_id', views.update_user_id, name='update_user_id'),
path('products/<str:municipality_name>/',views.shared_textarea,name='products'),
path('shared_textareas', views.shared_textareas, name='shared_textareas'),
path('shared_textareasdep', views.shared_textareasdep, name='shared_textareasdep'),
path('reply_textarea', views.ReplyForms, name='reply_textarea'),
path('emergency', views.emergency, name='emergency'),
path('deplogin', views.login_view_dept, name='deplogin'),
path('update_activity', views.update_activity, name='update_activity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)