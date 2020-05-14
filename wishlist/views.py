from django.shortcuts import render, get_object_or_404, redirect
from .models import Wishlist
from courses.models import Course
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def wishlistview(request):
    user = User.objects.get(username=request.user)
    wishlist = Wishlist.objects.get(user=user)

    all_courses = wishlist.course.all()

    return render(request, 'wishlist/main_wish.html', {'all_courses': all_courses})


@login_required
def add_wish(request, id, slug):
    user = User.objects.get(username=request.user)
    wishlist = Wishlist.objects.get(user=user)
    course = get_object_or_404(Course, id=id, slug=slug)

    wishlist.course.add(course)

    return redirect('wishlist:main_wishlist')


@login_required
def remove_wish(request, id, slug):
    user = User.objects.get(username=request.user)
    wishlist = Wishlist.objects.get(user=user)
    course = get_object_or_404(Course, id=id, slug=slug)

    wishlist.course.remove(course)

    return redirect('wishlist:main_wishlist')
