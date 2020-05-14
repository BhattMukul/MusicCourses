from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, related_name='courses', blank=True)

    def __str__(self):
        return str(self.user)
