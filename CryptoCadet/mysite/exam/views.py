from django.shortcuts import render, redirect
from .models import Question
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


from exam.models import Question
from exam.forms import ExamPaper

q1 = Question(primaryk=1, question = "1. abc", answer = "2", option_one= "1", option_two="2", option_three="3", option_four="4")

q2 = Question(primaryk=2, question = "2. def", answer = "3", option_one= "1", option_two="2", option_three="3", option_four="4")

q3 = Question(primaryk=3, question = "3. ghi", answer = "1", option_one= "1", option_two="2", option_three="3", option_four="4")

q4 = Question(primaryk=4, question = "4. jkl", answer = "4", option_one= "1", option_two="2", option_three="3", option_four="4")


def take_quiz(request):

    questionList = [q1, q2, q3, q4]
    context= {"questions": questionList}

    if request.method == 'GET':
        return render(request, 'exam.html',context)
    
    if request.method == 'POST':
        HttpResponse("thanks!")

def result(response):
    return render(response, 'resultPage.html')


def detail(request): 
    return HttpResponse(" hello ")

