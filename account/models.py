from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE,primary_key=True)
    #additional
    token=models.CharField(max_length=256)
    validatetime=models.DateTimeField()
    dob=models.DateField()
    profile_pic=models.ImageField(upload_to='profile',default="../static/img6Q.png",blank=True)
    def __str__(self):
        return "{0} {1}".format(self.user.first_name,self.user.last_name)