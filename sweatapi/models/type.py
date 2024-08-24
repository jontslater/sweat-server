from django.db import models

class Type(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name
