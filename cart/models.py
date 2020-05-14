from django.db import models
from courses.models import Course


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.cart_id


class Cart_Item(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def sub_total(self):
        return 1000

    def __str__(self):
        return self.course
