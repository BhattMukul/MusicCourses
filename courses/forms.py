from django.forms import ModelForm, Form
from django import forms
from .models import Course, Video, Review


class CourseAddForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'thumbnail',
                  'preview_video', 'language', 'requirements', 'description']


class VideoAddForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'order', 'video_length_in_min', 'video']

    def __init__(self, *args, **kwargs):
        super(VideoAddForm, self).__init__(*args, **kwargs)
        self.fields['video'].widget.attrs.update({
            'id': 'custom-file-input',
            'class': 'file_input',
            'name': 'file_input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review']


class RefundForm(forms.Form):
    refund_reason = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))
