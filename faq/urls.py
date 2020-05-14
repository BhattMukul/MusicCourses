from django.urls import path
from .views import AllFaqs, PartFaq

app_name = 'faq'

urlpatterns = [
    path('', AllFaqs, name='allfaqs'),
    path('<int:id>/', PartFaq, name='partfaq')
]
