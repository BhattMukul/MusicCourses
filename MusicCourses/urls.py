"""E_Learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from courses import views as course_view
from order import views as order_view
from account.views import support, supportsuccess

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls', namespace='courses')),
    path('accounts/', include('account.urls', namespace='account')),
    # password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password-reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password-reset-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password-reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password-reset-complete.html'), name='password_reset_complete'),

    # cart
    path('cart/', include('cart.urls', namespace='cart')),

    # order
    path('order/', include('order.urls', namespace='order')),

    # wishlist
    path('wishlist/', include('wishlist.urls', namespace='wishlist')),

    # Course New or Edit
    path('new-course/', course_view.course_add, name='course_add'),
    path('edit/<int:id>/<slug:slug>/',
         course_view.course_edit, name='course_edit'),
    path('edit/<int:id>/<slug:slug>/new-video/',
         course_view.video_add, name='video_add'),
    path('edit/<int:id>/<slug:slug>/edit-video/<int:video_id>',
         course_view.video_edit, name='video_edit'),

    # support

    path('support/', support, name='support'),
    path('support/success', supportsuccess, name='supportsuccess'),

    # refund Course

    path('admin-refund-course/', order_view.refund_course, name='refund_course'),
    path('admin-refund-course/<str:txn_id>',
         order_view.refund_course, name='refund_course_with_txnid'),
    path('admin-refund-course/<str:txn_id>/process/',
         order_view.refund_course_process, name='process_refund_course'),
    path('request-refund/<int:id>',
         course_view.request_refund, name='request_refund'),

    path('cannot-refund/', course_view.cannot_refund, name='cannot_refund'),
    path('process-refund/', course_view.process_refund, name='process_refund'),

    # FAQs

    path('faqs/', include('faq.urls', namespace='faq')),


    # Pay U Money

    path('payment/', include('payment.urls', namespace='payment')),

]
#  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
