from .models import Student


def student(request):
    if str(request.user) == 'AnonymousUser':
        st = None
    else:
        st = Student.objects.get(user__username=request.user)
    return {'st': st}
