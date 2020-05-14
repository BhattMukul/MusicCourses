from django.db import models


class Faq(models.Model):
    question = models.CharField(max_length=2000)
    answer1 = models.TextField()
    answer2 = models.TextField(blank=True, null=True)
    answer3 = models.TextField(blank=True, null=True)
    faq_img1 = models.ImageField(upload_to='faq', blank=True, null=True)
    faq_img2 = models.ImageField(upload_to='faq', blank=True, null=True)
    faq_img3 = models.ImageField(upload_to='faq', blank=True, null=True)

    def __str__(self):
        return self.question
