from django.shortcuts import render
from .models import Image


def index(request):
    images = Image.objects.all()
    return render(request, 'index.html', {'images': images})


def img_new(request):
    return render(request, 'img_new.html')


def img_view(request):
    return render(request, 'img_view.html')
