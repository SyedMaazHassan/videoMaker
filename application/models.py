from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Create your models here.


class authentication(models.Model):
    which_user = models.ForeignKey(User, on_delete = models.CASCADE)
    auth_code = models.CharField(max_length = 255)
    isCompleted = models.BooleanField(default = False)

class password_resetting(models.Model):
    which_user = models.ForeignKey(User, on_delete = models.CASCADE)
    reset_code = models.CharField(max_length = 255)

class user_fields(models.Model):
    input_name = models.CharField(max_length = 255)
    input_type = models.CharField(max_length = 100)
    code = models.CharField(max_length = 100)

class product(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="product_photos")
    previewLink = models.CharField(max_length = 255)
    price = models.FloatField()
    code = models.CharField(max_length = 100)

    def __str__(self):
        return self.title+" ("+str(self.price)+")"


# class order(models.Model):
#     which_product = models.ForeignKey(product, on_delete = models.CASCADE)
#     which_user = models.ForeignKey(User)
