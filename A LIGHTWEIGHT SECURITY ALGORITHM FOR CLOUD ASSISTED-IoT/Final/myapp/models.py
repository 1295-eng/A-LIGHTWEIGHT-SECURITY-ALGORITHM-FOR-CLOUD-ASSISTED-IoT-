from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
class Pulse(models.Model):
    name = models.CharField(max_length=20)
    pul = models.IntegerField(default=60)

    def __str__(self):
        return self.name
    
