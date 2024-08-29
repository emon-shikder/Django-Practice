from django.shortcuts import render
import datetime

# Create your views here.
def home(request):
    d = { 'val': ['python', 'is', 'fun'], 'Date': datetime.datetime.now(),'value':20, 'word': "emon", 'val1': "January - February - March", 'Name' : [
    {'name': 'Josh', 'age': 19},
    {'name': 'Dave', 'age': 22},
    {'name': 'Joe', 'age': 31},] ,
    'title':'Django rest framework', 
    'new' : "I'm Jai"}
    return render(request , 'first_app/home.html', d )