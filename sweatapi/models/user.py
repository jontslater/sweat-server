from django.db import models

class User(models.Model):
    username = models.CharField(max_length=55)
    email = models.EmailField(max_length=55)
    created_on = models.DateField(auto_now_add=True)
    uid = models.CharField(max_length=50)

    def __str__(self):
        return self.username
