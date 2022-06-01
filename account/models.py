from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserProfile(models.Model):
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE,primary_key=True)
    #additional
    token=models.CharField(max_length=256)
    validatetime=models.DateTimeField()
    dob=models.DateField()
    profile_pic=models.ImageField(upload_to='profile',default="../media/profile/img6Q.png",blank=True)
    def __str__(self):
        return "{0} {1}".format(self.user.first_name,self.user.last_name)
    # def save(self):
    #     super().save()
    #     img=Image.open(self.profile_pic.path)
    #     if(img.height>img.width):
    #         diff=img.height-img.width
    #         img=img.crop((0,diff/2,img.width,img.height-diff/2))
    #     else:
    #         diff=img.width-img.height
    #         img=img.crop((diff/2,0,img.width-diff/2,img.height))
    #     img.thumbnail((300,300))
    #     img.save(self.profile_pic.path)