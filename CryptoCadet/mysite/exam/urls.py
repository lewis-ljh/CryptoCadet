from django.urls import path
from exam.views import *

urlpatterns = [
    path('exam/', take_quiz, name='take_quiz'),
    path ('detail/', detail, name = 'detail'),
    path ('exam/results/', result, name='results')
]