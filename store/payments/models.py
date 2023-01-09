from django.db import models

# Create your models here.

class Payment(models.Model):

    status = models.CharField(max_length=255)
