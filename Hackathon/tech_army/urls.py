
from django.contrib import admin
from django.urls import path,include
from . import views
app_name='myapp'
urlpatterns = [
    
path('', views.index,name='index1'),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)