from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import POS_app.business.Actors.User as user
import POS_app.business.Items.Payment as payment
import POS_app.business.Items.Utils as utils
# Create your models here.

characters = ['!', '@', '$', '&', '*', '_']
def has_appropriate_characters(text: str):
    return any(char in characters for char in text) #does text contain any of those chars?

def has_numbers(text: str):
    return any(char.isdigit() for char in text)

def password_validator(value: str):
    if len(value) < 8: #the password must be at least 8 letters long
        raise ValidationError("The password is too short.")
    elif (has_appropriate_characters(value) ==  False):
        raise ValidationError("Please input at least one of the following: '!', '@', '$', '&', '*', '_'.")
    elif (has_numbers(value) == False):
        raise ValidationError("Please insert at least one number.")
    
class Employees(models.Model):
    e_id = models.AutoField(primary_key=True, serialize=False,
                            verbose_name="Employee ID")  # no need for BigAutoField
    _name = models.CharField(max_length=255, verbose_name="Employee Name")
    _login = models.EmailField(
        max_length=255, unique=True, verbose_name="Login")  # unique logins
    _password = models.CharField(max_length=255, validators=[password_validator],verbose_name="Password")
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


class Orders(models.Model):
    o_id = models.AutoField(primary_key=True, serialize=False,
                            verbose_name="Order ID")
    waiter = models.ForeignKey(
        # it is not actually checked - but it is from the admin site, from our site, we should and need to add checking for roles beforehand.
        Employees,  on_delete=models.CASCADE, verbose_name="Assigned Waiter")
    displayed_id = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        verbose_name="Displayed ID")  # 1 to 99
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at")
    ready_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Ready at")
    delivered_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Paid at")
    paid_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Paid at")
    archived_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Archived at")
    status = models.CharField(max_length=50, choices=[(
        s.name, s.value) for s in utils.OrderStatus], default=utils.OrderStatus.NEW, verbose_name="Status")
    is_takeaway = models.BooleanField(verbose_name="Is takeaway")
    scheduled_pick_up = models.DateTimeField(
        blank=True, null=True, verbose_name="Scheduled pick up")
    estimated_pick_up = models.DateTimeField(
        blank=True, null=True, verbose_name="Estimated pick up")
    table_no = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)], blank=True, default=1,
        verbose_name="Table number")  # for example
    notes = models.CharField(max_length=255, blank=True, null=True,
                             default="", verbose_name="Notes")


class MenuItems(models.Model):
    m_id = models.AutoField(
        primary_key=True, serialize=False, verbose_name="Menu Item ID")
    name = models.CharField(max_length=255, unique=True, verbose_name="Name") #can't have two burgers with just a different price lol
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(
        0)], verbose_name="Price")  # cannot be negative, basically Float
    currency = models.CharField(max_length=20, choices=[(
        c.name, c.value) for c in payment.Currency], default=payment.Currency.ZLOTY.name, verbose_name="Currency")
    prep_time_min = models.IntegerField(validators=[MinValueValidator(
        1)], verbose_name="Minimal preparation time in minutes")
    active = models.BooleanField(default=True, verbose_name="Active status")
    course = models.CharField(
        max_length=255, default="", verbose_name="Course")
    tax = models.DecimalField(max_digits=5, decimal_places=2,
                              validators=[MinValueValidator(0)], default=8.0, verbose_name="Tax")


class OrderItems(models.Model):
    oi_id = models.AutoField(
        primary_key=True, serialize=False, verbose_name="Order Item ID")
    m_id = models.ForeignKey(MenuItems, on_delete=models.PROTECT,
                             verbose_name="FK Menu Item ID")  # or models.DO_NOTHING
    quantity = models.DecimalField(max_digits=3, decimal_places=0,
                                   validators=[MinValueValidator(1)], default=1, verbose_name="Quantity")
    status = models.CharField(max_length=50, choices=[(
        s.name, s.value) for s in utils.OrderStatus], default=utils.OrderStatus.NEW, verbose_name="Status")
    ready_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Ready at")


class ServingRules(models.Model):
    s_id = models.AutoField(
        primary_key=True, serialize=False, verbose_name="Serving Rules ID")
    o_id = models.ForeignKey(Orders, on_delete=models.PROTECT,
                             verbose_name="FK Order ID")
    oi_id = models.ForeignKey(OrderItems, on_delete=models.DO_NOTHING,
                              # actually unsure about the course of action here, do we delete the order item?
                              verbose_name="FK Order Item ID")
    position = models.DecimalField(max_digits=3, decimal_places=0,
                                   validators=[MinValueValidator(1)], default=1, verbose_name="Position")
    course = models.CharField(
        # unsure about its importance here
        max_length=255, default="", verbose_name="Course")


class Payments(models.Model):
    p_id = models.AutoField(
        primary_key=True, serialize=False, verbose_name="Payment ID")
    o_id = models.ForeignKey(Orders, on_delete=models.PROTECT,
                             verbose_name="FK Order ID")
    total = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(
        0)], verbose_name="Total Price")
    currency = models.CharField(max_length=20, choices=[(
        c.name, c.value) for c in payment.Currency], default=payment.Currency.ZLOTY.name, verbose_name="Currency")
    paid_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Paid at")
