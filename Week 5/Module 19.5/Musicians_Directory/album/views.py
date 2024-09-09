from django.shortcuts import render, redirect
from .models import Album
from .forms import AlbumForm

def create_album(request):
    form = AlbumForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'album/form.html', {'form': form})

def edit_album(request, id):
    album = Album.objects.get(id=id)
    form = AlbumForm(request.POST or None, instance=album)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'album/form.html', {'form': form})

def delete_album(request, id):
    album = Album.objects.get(id=id)
    album.delete()
    return redirect('home')
