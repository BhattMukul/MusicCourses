from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.signin_view, name='login'),
    path('login/wrong/', views.signin_view_wrong, name='login_wrong'),
    path('logout/', views.signout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('instructor/', views.instructor_profile, name='instructor_profile'),
    path('instructor/done', views.create_instructor, name='create_instructor'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('request_transfer/<int:id>',
         views.request_transfer, name='request_transfer'),
    path('request_transfer_confirm/<int:id>', views.request_transfer_confirm,
         name='request_transfer_confirm'),
    path('request_transfer/success', views.request_transfer_success,
         name='request_transfer_success'),
    path('request_transfer/not-valid', views.request_transfer_fail,
         name='request_transfer_fail'),
]
