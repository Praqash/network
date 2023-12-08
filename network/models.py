from xmlrpc.client import Boolean
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from PIL import Image
from PIL.ExifTags import TAGS




class User(AbstractUser):
    followed = models.ManyToManyField('self', symmetrical=False, related_name='user_followed')
    
class Post(models.Model): 
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='post_like')
    followed = models.ManyToManyField(User, default=None, blank=True, related_name='post_followed')
    like_count = models.BigIntegerField(default='0')
    content = models.TextField(blank=False)
    
    def __str__(self):
        return '{} {}'.format(self.username, self.content)

class Profile(models.Model):
    username = models.OneToOneField(User, primary_key= True, null = False, on_delete=models.CASCADE)
    name=models.CharField(max_length=100, default=None,null= True, blank= True)
    status=models.CharField(max_length=120, default="Hi Iam using Network!")
    gender=models.CharField(max_length=120, default=None, blank= True, null= True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_picture.path)

        # Check for EXIF orientation
        try:
            for orientation in TAGS.keys():
                if TAGS[orientation] == 'Orientation':
                    break
            exif = dict(img._getexif().items())

            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # No EXIF data or orientation tag found
            pass

        # Resize the image
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

    def __str__(self):
        return '{} {}'.format(self.username, self.name)
    



