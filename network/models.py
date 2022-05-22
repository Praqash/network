from xmlrpc.client import Boolean
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone




class User(AbstractUser):
    pass
class Post(models.Model): 
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default = timezone.now)
    likes=models.ManyToManyField(User, default=None, blank = True, related_name='like')
    followed=models.ManyToManyField(User, default=None, blank = True, related_name='followed')
    like_count=models.BigIntegerField(default='0')
    content=models.TextField(blank= False)
    def __str__(self):
        return '{} {}'.format(self.username, self.content)

class Profile(models.Model):
    username = models.CharField(max_length=100, primary_key= True, default=None)
    name=models.CharField(max_length=100, default=None,null= True, blank= True)
    status=models.CharField(max_length=120, default="Hi Iam using Network!")
    gender=models.CharField(max_length=120, default=None, blank= True, null= True)
    def __str__(self):
        return '{} {}'.format(self.followed, self.follower)
    

    



