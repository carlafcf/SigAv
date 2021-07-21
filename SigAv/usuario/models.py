from django.db import models
from django.contrib import auth

class Usuario(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name', 'last_name']