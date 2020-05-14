from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from .forms import SignUpForm, ProfileImgForm, InstructorProfileForm, SupportForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import Instructor, Student, MoneyTransfer
from django.contrib.auth.decorators import login_required
from courses.models import Course
from wishlist.models import Wishlist
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings
from django.http import HttpResponseRedirect


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signupuser = User.objects.get(username=username)
            student_group = Group.objects.get(name='Student')
            student_group.user_set.add(signupuser)

            student = Student.objects.create(user=signupuser)
            wishlist = Wishlist.objects.create(user=signupuser)

            return redirect('account:login')

    else:
        form = SignUpForm()

    return render(request, 'account/st_register.html', {'form': form})


def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:user_profile')
        else:
            return redirect('http://127.0.0.1:8000/accounts/login/wrong/')

    else:
        form = AuthenticationForm()

    return render(request, 'account/login.html', {'form': form})


def signin_view_wrong(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:user_profile')
        else:
            return redirect('http://127.0.0.1:8000/accounts/login/wrong/')

    else:
        form = AuthenticationForm()

    return render(request, 'account/login_wrong.html', {'form': form})


@login_required
def signout_view(request):
    logout(request)
    return redirect('account:login')


@login_required
def user_profile(request):
    person = request.user
    student = get_object_or_404(Student, user__username=person)
    if request.method == 'POST':
        form = ProfileImgForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('account:user_profile')
    else:
        form = ProfileImgForm()
    # student = Student.objects.get(user__username=person)

    return render(request, 'account/user_profile.html', {'student': student, 'form': form})


@login_required
def create_instructor(request):
    username = request.user
    person = User.objects.get(username=username)
    instructor = Instructor.objects.create(user=person)
    instructor_group = Group.objects.get(name='Instructor')
    instructor_group.user_set.add(person)

    return redirect('account:instructor_profile')


@login_required
def instructor_profile(request):
    form = None
    instructor = None
    is_instructor = None
    username = request.user
    person = User.objects.get(username=username)
    try:
        instructor = Instructor.objects.get(user=person)
        is_instructor = True
        form = InstructorProfileForm(instance=instructor)
        if request.method == 'POST':
            form = InstructorProfileForm(request.POST, instance=instructor)
            if form.is_valid():
                pic = form.save(commit=False)
                student = get_object_or_404(Student, user=person)
                profile_pic = student.profile_pic
                pic.profile_pic = profile_pic
                pic.save()
    except:
        is_instructor = None
    return render(request, 'account/instructor_profile.html', {'instructor': instructor, 'form': form, 'is_instructor': is_instructor})


@login_required
def my_courses(request):
    return render(request, 'account/my_courses.html')


def support(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            issue = form.cleaned_data['issue']
            description = form.cleaned_data['description']

            # email

            subject = 'MusiLearn Support'
            to = ['mb.musilearn@gmail.com']
            # from_email = str(settings.EMAIL_HOST_USER)
            from_email = 'MusiLearn ' + '<' + \
                str(settings.EMAIL_HOST_USER) + '>'

            ctx = {
                'name': str(name),
                'email': str(email),
                'issue': str(issue),
                'desc': str(description),

            }

            message = get_template(
                'email/support.html').render(context=ctx)
            msg = EmailMessage(
                subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()

            return redirect('supportsuccess')

    else:
        form = SupportForm()

    return render(request, 'account/support.html', {'form': form})


def supportsuccess(request):
    return render(request, 'account/support_success.html')


@login_required
def request_transfer(request, id):
    user = User.objects.get(username=request.user)
    try:
        instructor = Instructor.objects.get(user=user)
        if instructor.credits_15 >= 5000:
            return redirect('account:request_transfer_confirm', id=id)
        else:
            return redirect('account:request_transfer_fail')
    except:
        return redirect('courses:index')


@login_required
def request_transfer_confirm(request, id):
    user = User.objects.get(username=request.user)
    instructor = Instructor.objects.get(user=user)
    if instructor:
        if instructor.credits_15 >= 5000:
            if request.method == 'POST':
                money = MoneyTransfer.objects.create(
                    instructor=instructor,
                    amount=instructor.credits_15,
                )
                money.save()

                instructor.last_requested = timezone.now()
                instructor.save()

                # email
                subject = 'MusiLearn Amount Transfer'
                to = ['mb.musilearn@gmail.com']
                from_email = 'MusiLearn ' + '<' + \
                    str(settings.EMAIL_HOST_USER) + '>'

                ctx = {
                    'instructor': instructor
                }

                message = get_template(
                    'email/amount_request.html').render(context=ctx)
                msg = EmailMessage(
                    subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()

                instructor.credits_15 = 0
                instructor.save()

                return redirect('account:request_transfer_success')

            return render(request, 'account/request_transfer_confirm.html', {'instructor': instructor})
        else:
            return HttpResponseRedirect(request.path_info)
    else:
        return redirect('courses:index')


@login_required
def request_transfer_success(request):
    return render(request, 'account/request_transfer_success.html')


def request_transfer_fail(request):
    return render(request, 'account/request_transfer_fail.html')
