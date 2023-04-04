from django.db import models

# Create your models here.

class Exam (models.Model):
    name = models.CharField(max_length = 100)

    def __str__ (self):
        return self.name
    

class Question(models.Model): 
    primaryk = models.IntegerField(max_length=10)
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=100)
    option_one = models.CharField(max_length=100)
    option_two = models.CharField(max_length=100)
    option_three = models.CharField(max_length=100, blank=True)
    option_four = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.question
    



