from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Blog(models.Model):
    blogger=models.ForeignKey(User,related_name='blogs',on_delete=models.CASCADE)
    title=models.CharField(max_length=256)
    description=models.CharField(max_length=256)
    body=models.TextField()
    datetime=models.DateTimeField()
    img=models.ImageField(upload_to='blogimage')
    def __str__(self):
        return "{0} {1}".format(self.blogger.username,self.title)
    def save(self):
        super().save()
        img=Image.open(self.img.path)
        img.thumbnail((1600,900))
        img.save(self.img.path)