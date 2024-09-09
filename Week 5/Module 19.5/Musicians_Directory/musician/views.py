from django.shortcuts import render, redirect
from .models import Musician
from .forms import MusicianForm

def create_musician(request):
    if request.method == 'POST':
        form = MusicianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MusicianForm()
    return render(request, 'musician/form.html', {'form': form})

def edit_musician(request, id):
    musician = Musician.objects.get(id=id)
    form = MusicianForm(request.POST or None, instance=musician)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'musician/form.html', {'form': form})

def delete_musician(request, id):
    musician = Musician.objects.get(id=id)
    musician.delete()
    return redirect('home')
