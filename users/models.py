from django.db import models

class AppUsers(models.Model):

    name = models.CharField(max_length=20, null=False,blank=False)
    pwd = models.CharField(max_length=30, null =False, blank=False)
    occupation = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name