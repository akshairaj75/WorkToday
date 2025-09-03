from datetime import timezone
from tkinter.constants import CASCADE

from django.db import models
# Create your models here.

class category(models.Model):
    category_name = models.CharField(max_length=200)

class user(models.Model):
    username = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    phone = models.IntegerField()

class job(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(null=True)
    time = models.CharField(max_length=200,null=True)
    location = models.CharField(max_length=200)
    wage = models.IntegerField(null=True)
    vacancy = models.IntegerField(null=True)
    category = models.ForeignKey(category,on_delete = models.CASCADE,null=True)
    description = models.TextField(max_length=200)
    user_recruiter = models.ForeignKey(user,on_delete=models.CASCADE,null=True)

class applications(models.Model):
    job = models.ForeignKey(job,on_delete=models.CASCADE)
    applicant = models.ForeignKey(user, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200,null=True)






