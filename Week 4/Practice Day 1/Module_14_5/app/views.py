from django.shortcuts import render
from .forms import ExampleForm,GeeksForm

# Create your views here.

def home(request):
    form1 = ExampleForm()
    form2 = GeeksForm()

    return render(request, 'app/home.html', {'form': form1, 'form1': form2})