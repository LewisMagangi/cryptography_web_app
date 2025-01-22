# Create your models here

from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class SymmetricAnalysisResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    algorithm = models.CharField(max_length=50)
    operation = models.CharField(max_length=50)
    key_size = models.IntegerField()
    file_name = models.CharField(max_length=100)
    time_taken = models.FloatField()

    def __str__(self):
        return f"{self.algorithm} - {self.operation} - {self.key_size} - {self.file_name}"