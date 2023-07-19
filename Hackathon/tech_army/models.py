from django.db import models
from django.contrib.auth.models import User


class Society(models.Model):
    place_id=models.AutoField
    municipality_name=models.CharField(max_length=50)
    ward_no=models.CharField(max_length=50)
    desc=models.CharField(max_length=500)
    
    def __str__(self):
           return self.book_name
       
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    citizenship_id = models.CharField(max_length=20,default="")
    municipality_name=models.CharField(max_length=50)
    ward_no=models.CharField(max_length=50)
    image = models.ImageField(upload_to='myapp/images',default="")
    

    def __str__(self):
        return self.user.username