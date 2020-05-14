from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, Cart_Item
from account.models import Student
from courses.models import Course
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from order.models import Order, OrderItem
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


MERCHANT_KEY = 'IAj1ZlbUXqJibKTg'


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required
def add_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart.delete()
        cart = Cart.objects.create(
            cart_id=_cart_id(request),
        )
        cart.save()

    except:
        cart = Cart.objects.create(
            cart_id=_cart_id(request),
        )
        cart.save()

    cart_item = Cart_Item.objects.create(
        course=course,
        cart=cart
    )

    cart_item = Cart_Item.objects.get(
        course=course,
        cart=cart
    )

    cart_item.save()
    return redirect('cart:cart_detail')


@login_required
def CartDetail(request, cart_item=None, total=0):
    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )
        cart_item = Cart_Item.objects.filter(cart=cart, active=True)
        total = cart_item[0].course.price
        if request.method == 'POST':
            refund_period = timezone.now() + timezone.timedelta(days=3)
            try:
                person = request.user
                user = User.objects.get(username=person)
                order_detail = Order.objects.create(
                    user=user,
                    total=total,
                    refund_period=refund_period,
                )
                order_detail.save()

                for order_item in cart_item:
                    oi = OrderItem.objects.create(
                        course=order_item.course,
                        price=order_item.course.price,
                        order=order_detail,
                    )
                    student = Student.objects.get(user=user)

                    oi.save()

                cart.delete()
                return redirect('payment:main_payment', user_id=order_detail.user.id, id=order_detail.id)
            except ObjectDoesNotExist:
                pass

    except ObjectDoesNotExist:
        pass
    return render(request, 'cart/cart_detail.html', {'cart_item': cart_item, 'total': total})


@login_required
def cart_empty(request):
    cart = None
    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )
    except ObjectDoesNotExist:
        pass

    cart.delete()
    return redirect('cart:cart_detail')
