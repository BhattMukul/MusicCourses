from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/students', default='https://musilearn-bucket.s3.amazonaws.com/static/img/user.png')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/instructors', blank=True, null=True, default='https://musilearn-bucket.s3.amazonaws.com/static/img/user.png')
    about_yourself = models.TextField(blank=True)
    age = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    bank_account_name = models.CharField(max_length=300, blank=True, null=True)
    bank_name = models.CharField(max_length=300, blank=True)
    bank_account_number = models.CharField(
        max_length=20, blank=True, null=True)
    bank_account_type = models.CharField(max_length=200, default='Saving')
    IFSC_code = models.CharField(max_length=15, blank=True, null=True)
    total_credits = models.IntegerField(default=0)
    credits_15 = models.IntegerField(default=0)
    last_requested = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class MoneyTransfer(models.Model):
    instructor = models.ForeignKey(
        Instructor, related_name='instructor', on_delete=models.DO_NOTHING)
    amount = models.PositiveIntegerField()
    requested = models.DateTimeField(auto_now=True)
    transfered = models.BooleanField(default=False)
