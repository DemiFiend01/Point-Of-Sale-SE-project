from django.db import models
import POS_app.business.Actors.User as user
# Create your models here.
class Employees(models.Model):
    _name = models.CharField(max_length=255)
    _login = models.CharField(max_length=255)
    _password = models.CharField(max_length=255)
    _role = models.CharField(
        max_length=50,
        choices=[(r.name, r.value) for r in user.Role]
    )