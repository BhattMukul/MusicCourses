from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import Instructor, Student


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    meta_desc = models.CharField(max_length=160, blank=True, null=True)
    meta_key = models.CharField(max_length=210, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses:courses_by_category', kwargs={'category_slug': self.slug})


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tutor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name='tutor')
    title = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=2000, blank=True, null=True)
    language = models.CharField(max_length=200, default='English')
    thumbnail = models.ImageField(upload_to='course/thumbnail')
    preview_video = models.FileField(upload_to='video/previews', blank=True)
    requirements = models.TextField(default='Type Course Requirements Here')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student,  related_name='students')
    price = models.IntegerField(default=1000)
    total_rating = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)+' by '+str(self.tutor.user.first_name)+' '+str(self.tutor.user.last_name)

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'id': self.id, 'slug': self.slug})

    def get_rating(self):
        return self.total_rating * '*'

    def get_course_content(self):
        return reverse('courses:course_content_redirect', kwargs={'id': self.id, 'slug': self.slug})


class Video(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course')
    title = models.CharField(max_length=1000)
    order = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    video_length_in_min = models.IntegerField(default=1)
    video = models.FileField(
        upload_to='course/videos')

    def __str__(self):
        return str(self.course.title)+'-'+str(self.title)

    def get_absolute_url(self):
        return reverse('courses:course_content', kwargs={'id': self.course.id, 'slug': self.course.slug, 'video_id': self.id})


class Rating(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(default=None)

    def __str__(self):
        return str(self.user)


class Review(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.user)
