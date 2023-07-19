
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tech_army.urls')),
    path('myapp', include('tech_army.urls')),
]
