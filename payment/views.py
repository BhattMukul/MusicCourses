from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template, RequestContext
import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
from order.models import Order, OrderItem
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from account.models import Student, Instructor


def main_payment(request, user_id, id):
    user = User.objects.get(id=user_id)
    order = Order.objects.get(id=id, user=user)
    order_item = OrderItem.objects.get(order=order)
    course = order_item.course
    total = str(order.total)+'.00'
    MERCHANT_KEY = "QEvPOtFK"
    key = "QEvPOtFK"
    SALT = "o3hJWK8Fsn"
    PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
    action = ''
    posted = {}
    posted['amount']: total
    success_url = 'http://127.0.0.1:8000/payment/Success/'
    fail_url = 'http://127.0.0.1:8000/payment/Failure/'
    # Merchant Key and Salt provided y the PayU.
    if request.method == 'POST':
        for i in request.POST:
            posted[i] = request.POST[i]
        hash_object = hashlib.sha256(b'randint(0,20)')
        txnid = hash_object.hexdigest()[0:20]
        hashh = ''
        posted['txnid'] = txnid
        hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        posted['key'] = key
        hash_string = ''
        hashVarsSeq = hashSequence.split('|')
        for i in hashVarsSeq:
            try:
                hash_string += str(posted[i])
            except Exception:
                hash_string += ''
            hash_string += '|'
        hash_string += SALT
        hashh = hashlib.sha512(
            hash_string.encode('utf-8')).hexdigest().lower()
        action = PAYU_BASE_URL
    if(posted.get("key") != None and posted.get("txnid") != None and posted.get("productinfo") != None and posted.get("firstname") != None and posted.get("email") != None):
        return render(request, 'payment/checkout.html', {'course': course, 'order': order, 'amount': total, "posted": posted, "hashh": hashh, "MERCHANT_KEY": MERCHANT_KEY, "txnid": txnid, "hash_string": hash_string, "action": action, 'success_url': success_url, 'fail_url': fail_url})
    else:
        return render(request, 'payment/checkout.html', {'course': course, 'order': order, 'amount': total, "action": "."})


@csrf_protect
@csrf_exempt
def payment_success(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "o3hJWK8Fsn"
    payuMoneyId = request.POST['payuMoneyId']
    order_id = int(productinfo)
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges+'|'+salt+'|'+status+'|||||||||||' + \
            email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
        retHashSeq = salt+'|'+status+'|||||||||||'+email+'|' + \
            firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if(hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        order = Order.objects.get(id=order_id)
        order_item = OrderItem.objects.get(order=order)
        student = Student.objects.get(user=order.user)
        order_item.course.students.add(student)
        order_item.course.tutor.total_credits += 400
        order_item.course.tutor.credits_15 += 400
        order_item.course.tutor.save()
        order.txn_id = payuMoneyId
        order.paid = True
        order.save()
        # sending notification email to the course tutor

        subject = 'MusiLearn Course Sold - '+str(order_item.course.title)
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
            'email/purchase_email.html').render(context=ctx)
        msg = EmailMessage(
            subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

    return render(request, 'payment/success.html', {"txnid": txnid, "status": status, "amount": amount, 'order_id': order_id})


@csrf_protect
@csrf_exempt
def payment_failure(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "o3hJWK8Fsn"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges+'|'+salt+'|'+status+'|||||||||||' + \
            email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
        retHashSeq = salt+'|'+status+'|||||||||||'+email+'|' + \
            firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if(hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        pass
    return render(request, "payment/Failure.html",  c)
