from django.shortcuts import render, redirect
from musician.models import Musician
from album.models import Album
from musician.forms import MusicianForm
from album.forms import AlbumForm

def home(request):
    musicians = Musician.objects.all()
    albums = Album.objects.all()
    return render(request, 'home/index.html', {
        'musicians': musicians,
        'albums': albums
    })
