from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Course, Video, Review, Rating
import random
from django.urls import reverse
from account.models import Student, Instructor
from django.db.models import Q
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from .forms import CourseAddForm, VideoAddForm, ReviewForm, RefundForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from order.models import Order, OrderItem
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings


def index(request):
    object_list = Course.objects.all()
    object_list = object_list.filter(active=True)
    course_num = object_list.count()
    cs = sorted(object_list, key=lambda x: random.random())
    cs = cs[:8]
    latest = object_list.order_by('-created')[:4]
    popular = object_list.order_by('students', 'total_rating')[:4]
    # instructors = len(Instructor.objects.all())
    # students = len(Student.objects.all())
    instructors = Instructor.objects.all().count()
    students = Student.objects.all().count()

    return render(request, 'courses/index.html', {'courses': cs,
                                                  'latest': latest,
                                                  'popular': popular,
                                                  'instructors': instructors,
                                                  'students': students,
                                                  'course_num': course_num})


def courses_by_category(request, category_slug=None, cate=None):
    try:
        courses = Course.objects.all()
        courses = courses.filter(active=True)
        q = None
        qq = None
        courses = courses.order_by('-total_rating', '-created')
        if category_slug:
            cate = get_object_or_404(Category, slug=category_slug)
            courses = courses.filter(category=cate)

        if 'query' in request.GET:
            q = request.GET.get('query')
            qq = q
            courses = courses.filter(
                Q(title__icontains=q) | Q(description__icontains=q))

        course_count = courses.count()
        paginator = Paginator(courses, 10)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except InvalidPage:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

    except:
        courses = None
        course_count = 0

    return render(request, 'courses/by_category.html', {'q': qq, 'course_count': course_count, 'courses': page_obj, 'category_slug': category_slug, 'cate': cate})


def course_detail(request, id, slug):
    owned = None
    tutor = None
    course = get_object_or_404(Course, id=id, slug=slug)
    recommend = Course.objects.filter(category=course.category)
    recommend = recommend.exclude(id=course.id)
    recommend = recommend.order_by('total_rating')[:3]
    duration = 0
    videos = Video.objects.filter(course=course)
    for video in videos:
        duration += int(video.video_length_in_min)
    person = request.user
    reviews = Review.objects.filter(course=course)
    if str(person) != 'AnonymousUser':
        login_user = User.objects.get(username=person)
        if login_user == course.tutor.user:
            owned = True
            tutor = True
        students = course.students.values_list('user', flat=True)
        if login_user.id in students:
            owned = True
    return render(request, 'courses/course-detail.html', {'duration': duration, 'recommend': recommend, 'reviews': reviews, 'owned': owned, 'course': course, 'videos': videos, 'tutor': tutor})


@login_required
def course_content_redirect(request, id, slug):
    course = get_object_or_404(Course, id=id, slug=slug, active=True)
    tutor = course.tutor
    person = request.user
    try:

        login_user = User.objects.get(username=person)

        students = course.students.values_list('user', flat=True)

        if login_user.id in students or login_user == tutor.user:

            video = Video.objects.filter(course=course)[0]

            video_id = video.id

            return redirect('courses:course_content', id=id, slug=slug, video_id=video_id)
        else:
            return redirect('courses:course_detail', id=id, slug=slug)
    except:
        return redirect('courses:course_detail', id=id, slug=slug)
    return redirect('courses:course_content', id=id, slug=slug, video_id=video_id)


@login_required
def course_content(request, id, slug, video_id):
    can_refund = None
    rated = None
    reviews = None
    course = get_object_or_404(Course, id=id, slug=slug, active=True)
    person = request.user
    tutor = course.tutor
    try:
        login_user = User.objects.get(username=person)
        students = course.students.values_list('user', flat=True)
        student = Student.objects.get(user=login_user)
        if login_user.id in students or login_user == tutor.user:
            videos = Video.objects.filter(course=course)
            videos = videos.order_by('order')
            current_video = Video.objects.get(id=video_id)
            # refund query
            orders = Order.objects.filter(
                user=login_user, order_items__course=course)

            order = orders[0]
            print(orders)
            refund_period = order.refund_period

            time = timezone.now()

            if time <= refund_period:

                can_refund = True

            else:
                can_refund = False

            # review
            form = ReviewForm()

            if request.method == 'POST':
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review_comment = request.POST.get('review')
                    revieww = Review.objects.create(
                        review=review_comment,
                        course=course,
                        user=student
                    )
                    return HttpResponseRedirect(request.path_info)

            course_rating = 0

            if 'rate' in request.GET:
                rate = int(request.GET.get('rate'))
                rating = Rating.objects.create(
                    rating=rate,
                    course=course,
                    user=student
                )
                ratings = Rating.objects.filter(course=course)
                total_rating = len(ratings)
                for r in ratings:
                    course_rating += int(r.rating)
                course_rating = (course_rating)//total_rating
                course.total_rating = course_rating
                course.save()
                return HttpResponseRedirect(request.path_info)
            try:
                rated = Rating.objects.get(course=course, user=student)
            except:
                rated = None
            reviews = Review.objects.filter(course=course)

        else:
            return redirect('courses:course_detail', id=id, slug=slug)
    except:
        return redirect('courses:course_detail', id=id, slug=slug)

    return render(request, 'courses/course_content.html', {'can_refund': can_refund, 'rated': rated, 'course': course, 'form': form, 'videos': videos, 'current_video': current_video, 'video_id': video_id, 'reviews': reviews})


@login_required
def course_add(request):
    time = timezone.now()
    thislist = str(time).split('.')
    thistime = str(thislist[0])
    timesigns = ['-', ':', '+', '.', ' ']
    for timesign in timesigns:
        thistime = thistime.replace(timesign, '')

    username = request.user
    user = User.objects.get(username=username)
    try:
        tutor = Instructor.objects.get(user=user)
        if request.method == 'POST':
            form = CourseAddForm(request.POST, request.FILES)
            if form.is_valid():
                course = form.save(commit=False)
                title = str(form.cleaned_data['title'])
                title_list = title.split(' ')
                title = '-'.join(title_list)
                slug = str(title)+'-'+thistime
                slug = slug.lower()
                course.tutor = tutor
                course.slug = slug
                course.save()

                return redirect('course_edit', id=course.id, slug=course.slug)
        else:
            form = CourseAddForm()
    except:
        return redirect('account:instructor_profile')

    return render(request, 'courses/course_add.html', {'form': form})


def course_edit(request, id, slug):
    course = None
    username = request.user
    user = User.objects.get(username=username)
    try:
        tutor = Instructor.objects.get(user=user)
        course = get_object_or_404(Course, id=id, slug=slug, tutor=tutor)
        videos = Video.objects.filter(course=course)
        videos = videos.order_by('order')
        form = CourseAddForm(instance=course)
        if request.method == 'POST':
            form = CourseAddForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                course = form.save(commit=False)
                title = str(form.cleaned_data['title'])
                title_list = title.split(' ')
                title = '-'.join(title_list)
                slug = str(username)+'-'+str(title)
                slug = slug.lower()
                course.tutor = tutor
                course.slug = slug
                course.save()

                return HttpResponseRedirect(request.path_info)
    except:
        return redirect('account:my_courses')

    return render(request, 'courses/course_edit.html', {'form': form, 'course': course, 'videos': videos})


@login_required
def video_add(request, id, slug):
    user = User.objects.get(username=request.user)
    videos = None
    try:
        tutor = Instructor.objects.get(user=user)
        course = Course.objects.get(id=id, slug=slug, tutor=tutor)
        if request.method == 'POST':
            form = VideoAddForm(request.POST, request.FILES)
            if form.is_valid():
                video = form.save(commit=False)
                video.course = course
                video.save()
                course.active = True
                course.save()
                return redirect('course_edit', id=id, slug=slug)
        else:
            form = VideoAddForm()

    except ObjectDoesNotExist:
        return redirect('account:instructor_profile')

    except:
        return redirect('account:instructor_profile')

    return render(request, 'courses/add_video.html', {'course': course, 'form': form})


@login_required
def video_edit(request, id, slug, video_id):
    video = None
    user = User.objects.get(username=request.user)
    try:
        tutor = Instructor.objects.get(user=user)
        course = Course.objects.get(id=id, slug=slug, tutor=tutor)
        video = Video.objects.get(id=video_id)
        if request.method == 'POST':
            form = VideoAddForm(request.POST, request.FILES, instance=video)
            if form.is_valid():
                video = form.save(commit=False)
                video.course = course
                video.save()
                return redirect('course_edit', id=id, slug=slug)
        else:
            form = VideoAddForm(instance=video)

    except ObjectDoesNotExist:
        return redirect('account:instructor_profile')

    except:
        return redirect('account:instructor_profile')

    return render(request, 'courses/video_edit.html', {'course': course, 'form': form, 'video': video})


@login_required
def request_refund(request, id):
    form = None
    course = get_object_or_404(Course, id=id)
    person = request.user
    try:
        login_user = User.objects.get(username=person)
        students = course.students.values_list('user', flat=True)
        student = Student.objects.get(user=login_user)
        if login_user.id in students:
            # refund query
            orders = Order.objects.filter(
                user=login_user, order_items__course=course)

            # for orde in orders:
            #     order = orde
            order = orders[0]
            refund_period = order.refund_period
            time = timezone.now()
            if time <= refund_period:
                form = RefundForm()
                if request.method == 'POST':
                    form = RefundForm(request.POST)
                    if form.is_valid():
                        refund_reason = form.cleaned_data['refund_reason']
                        # email
                        subject = 'Request Refund'
                        to = ['mb.musilearn@gmail.com']
                        from_email = 'MusiLearn ' + '<' + \
                            str(settings.EMAIL_HOST_USER) + '>'

                        ctx = {
                            'username': str(login_user.username),
                            'email': str(login_user.email),
                            'order_id': str(order.id),
                            'txn_id': str(order.txn_id),
                            'course': course,
                            'reason': refund_reason,

                        }

                        message = get_template(
                            'email/request_refund.html').render(context=ctx)
                        msg = EmailMessage(
                            subject, message, to=to, from_email=from_email)
                        msg.content_subtype = 'html'
                        msg.send()
                        return redirect('process_refund')

                return render(request, 'courses/request_refund.html', {'form': form, 'course': course})

            else:
                return redirect('cannot_refund')
        else:
            return redirect('cannot_refund')
    except:
        return redirect('cannot_refund')


def cannot_refund(request, reason=None):
    return render(request, 'courses/cannot_refund.html')


def process_refund(request):
    return render(request, 'courses/process_refund.html')
