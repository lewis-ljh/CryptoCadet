from django.contrib import admin

from .models import Question, Exam

admin.site.register(Exam)
admin.site.register(Question)
