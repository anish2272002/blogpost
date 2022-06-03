from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField

CROP_SETTINGS = {'size': (300, 300), 'crop': 'smart'}

class UserProfile(models.Model):
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE,primary_key=True)
    #additional
    token=models.CharField(max_length=256)
    validatetime=models.DateTimeField()
    dob=models.DateField()
    profile_pic=ThumbnailerImageField(upload_to='profile',default="../media/profile/img6Q.png",blank=True,resize_source=CROP_SETTINGS)
    def __str__(self):
        return "{0} {1}".format(self.user.first_name,self.user.last_name)