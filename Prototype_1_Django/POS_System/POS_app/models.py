from django.db import models
from django.conf import settings

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    prep_time_min = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    course = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('AWAITING_PREPARATION', 'Awaiting preparation'),
        ('IN_PREPARATION', 'In preparation'),
        ('READY', 'Ready'),
        ('PAID', 'Paid'),
        ('ARCHIVED', 'Archived'),
        ('CANCELED', 'Canceled'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='NEW')

    is_takeaway = models.BooleanField(default=False)
    scheduled_pick_up = models.DateTimeField(null=True, blank=True)
    estimated_pick_up = models.DateTimeField(null=True, blank=True)

    table_no = models.CharField(max_length=10, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    ready_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id}"

    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def confirm(self):
        if self.status != 'NEW':
            raise ValueError("The order is not new")
        self.status = 'AWAITING_PREPARATION'
        self.save()

    def mark_paid(self):
        if self.status != 'READY':
            raise ValueError("The order is not ready yet.")
        self.status = 'PAID'
        self.paid_at = timezone.now()
        self.save()

    def archive(self):
        if self.status != 'PAID':
            raise ValueError("The order was not paid for, cannot archive.")
        self.status = 'ARCHIVED'
        self.archived_at = timezone.now()
        self.save()

    def cancel(self):
        if self.status in ('CANCELED', 'ARCHIVED'):
            raise ValueError("Cannot cancel already finished orders")
        self.status = 'CANCELED'
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    status = models.CharField(
        max_length=30,
        choices=Order.STATUS_CHOICES,
        default='NEW'
    )
    ready_at = models.DateTimeField(null=True, blank=True)
    course = models.CharField(max_length=50, blank=True)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.menu_item} (Order {self.order_id})"
