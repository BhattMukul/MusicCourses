from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


class Order(models.Model):
    txn_id = models.CharField(max_length=1000, blank=True)
    total = models.IntegerField(verbose_name='Total Amount')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    refund_period = models.DateTimeField(null=True)
    refunded = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    price = models.IntegerField()
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')

    def __str__(self):
        return str(self.course)
