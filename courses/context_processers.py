from .models import Category
from .models import Course
from account.models import Student
from django.contrib.auth.models import User


def category(request):
    categories = Category.objects.all()

    return {'categories': categories}


def my_courses(request):
    courses = None
    courses_by = None
    logged_in = None
    person = request.user
    if str(person) != 'AnonymousUser':
        logged_in = True
        user = User.objects.get(username=person)
        student = Student.objects.get(user=user)
        courses = Course.objects.filter(students__id=student.id)
        courses_by = Course.objects.filter(tutor__user=user)
    return {'mycourses': courses, 'mycourses_by': courses_by, 'logged_in': logged_in}
