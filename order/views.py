from django.shortcuts import render, redirect
from .models import Order, OrderItem
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .forms import RefundTxnidForm
from account.models import Student, Instructor
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.conf import settings
from django.utils import timezone


def order_success(request, id):
    order_id = id
    return render(request, 'order/success.html', {'order_id': order_id})


def order_unsuccess(request, reason=None):
    return render(request, 'order/unsuccess.html', {'reason': reason})


@user_passes_test(lambda u: u.is_superuser)
def refund_course(request, txn_id=None):
    order = None
    course = None
    thisuser = None
    form = RefundTxnidForm()
    if request.method == 'POST':
        form = RefundTxnidForm(request.POST)
        if form.is_valid():
            txn_id = form.cleaned_data['txn_id']
            return redirect('refund_course_with_txnid', txn_id=txn_id)

    if txn_id:
        form = RefundTxnidForm({'txn_id': txn_id})
        order = Order.objects.get(txn_id=txn_id)
        order_item = OrderItem.objects.get(order=order)
        course = order_item.course
        thisuser = order.user

    return render(request, 'order/refund.html', {'order': order,
                                                 'form': form,
                                                 'thisuser': thisuser,
                                                 'course': course, })


@user_passes_test(lambda u: u.is_superuser)
def refund_course_process(request, txn_id):
    order = Order.objects.get(txn_id=txn_id)
    order_item = OrderItem.objects.get(order=order)
    course = order_item.course
    user = order.user
    student = Student.objects.get(user=user)
    order_item.course.students.remove(student)
    order_item.course.tutor.total_credits -= 400
    order_item.course.tutor.credits_15 -= 400
    order_item.course.tutor.save()
    order.refunded = True
    order.save()

    # sending notification email to the course tutor and student

    subject = 'MusiLearn Course Refunded - '+str(order_item.course.title)
    to = [str(order_item.course.tutor.user.email)]
    from_email = 'MusiLearn ' + '<' + \
        str(settings.EMAIL_HOST_USER) + '>'

    ctx = {
        'student': student,
        'course': order_item.course,
        'datetime': str(timezone.now().date()),
        'tutor': order_item.course.tutor,
    }

    message = get_template(
        'email/tutor_refund_email.html').render(context=ctx)
    msg = EmailMessage(
        subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    subject = 'MusiLearn Course Refunded - '+str(order_item.course.title)
    to = [str(student.user.email)]
    from_email = 'MusiLearn ' + '<' + \
        str(settings.EMAIL_HOST_USER) + '>'

    ctx = {
        'student': student,
        'course': order_item.course,
        'datetime': str(timezone.now().date()),
    }

    message = get_template(
        'email/student_refund_email.html').render(context=ctx)
    msg = EmailMessage(
        subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    return redirect('refund_course')
