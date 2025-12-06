from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import POS_app.business.Actors.User as user
# Create your models here.


class Employees(models.Model):
    e_id = models.AutoField(primary_key=True, serialize=False,
                            verbose_name="Employee ID")  # no need for BigAutoField
    _name = models.CharField(max_length=255, verbose_name="Employee Name")
    _login = models.CharField(
        max_length=255, unique=True, verbose_name="Login")  # unique logins
    _password = models.CharField(max_length=255, verbose_name="Password")
    _role = models.CharField(
        max_length=50,
        choices=[(r.name, r.value) for r in user.Role], verbose_name="Employee Role"
    )

    def set_password(self, raw_pass):
        self._password = make_password(raw_pass)

    def check_password(self, raw_pass):
        # if we want to check the hashed password with the unhashed that the user just gave us
        return check_password(raw_pass, self._password)

    def save(self, *args, **kwargs):  # override the default Django method
        if not self._password.startswith('pbkdf2_'):  # default hashing method
            self._password = make_password(self._password)
        super().save(*args, **kwargs)  # call the default Django method
