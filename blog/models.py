from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField

CROP_SETTINGS = {'size': (1600, 900), 'crop': 'smart'}

class Blog(models.Model):
    id=models.BigAutoField(primary_key=True)
    blogger=models.ForeignKey(User,related_name='blogs',on_delete=models.CASCADE)
    title=models.CharField(max_length=256)
    description=models.CharField(max_length=256)
    body=models.TextField()
    datetime=models.DateTimeField()
    image=ThumbnailerImageField(upload_to='blogimage',blank=True,resize_source=CROP_SETTINGS)
    def __str__(self):
        return "{0} {1}".format(self.blogger.username,self.title)

class Comment(models.Model):
    id=models.BigAutoField(primary_key=True)
    blogger=models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,related_name='comments',on_delete=models.CASCADE)
    text=models.CharField(max_length=256)
    datetime=models.DateTimeField()
    def __str__(self):
        return "{0} {1} {2} {3}".format(self.blogger.username,self.blog.title,self.text,self.datetime)