from django.urls import path
from .views import index, courses_by_category, course_detail, course_content, course_content_redirect, course_add
app_name = 'courses'

urlpatterns = [
    path('', index, name='index'),
    path('category/', courses_by_category, name='courses_by_category_all'),
    path('category/<slug:category_slug>',
         courses_by_category, name='courses_by_category'),
    path('course/<int:id>/<slug:slug>', course_detail, name='course_detail'),
    path('course/<int:id>/<slug:slug>/lecture/',
         course_content_redirect, name='course_content_redirect'),
    path('course/<int:id>/<slug:slug>/lecture/<int:video_id>/',
         course_content, name='course_content'),


]
