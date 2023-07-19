
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name='tech_army'
urlpatterns = [
    
path('', views.index,name='index1'),
path('signup', views.signup, name='signup'),
path('login', views.login_view, name='login'),
path('logged', views.logged, name='logged'),
path('profile/', views.update_user_id, name='profile'),
path('update_user_id/', views.update_user_id, name='update_user_id'),
path('products',views.shared_textarea,name='products'),
path('shared_textarea', views.shared_textarea, name='shared_textarea'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)