from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class City(models.Model):
    name=models.CharField(max_length=30)
    author=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural='cities'
    