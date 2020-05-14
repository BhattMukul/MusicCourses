from django.shortcuts import render, get_object_or_404
from .models import Faq


def AllFaqs(request):
    allfaqs = Faq.objects.all()
    return render(request, 'faq/allfaqs.html', {'allfaqs': allfaqs})


def PartFaq(request, id):
    allfaqs = Faq.objects.all()
    faq = get_object_or_404(Faq, id=id)
    return render(request, 'faq/faq.html', {'faq': faq, 'allfaqs': allfaqs})
