from django.core.files.images import get_image_dimensions
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ImageForm, ImgForm
from .models import Image

import requests
from io import BytesIO
import PIL


def index(request):
    images = Image.objects.all()
    return render(request, 'index.html', {'images': images})


def img_new(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['img'] and form.cleaned_data['link']:
                return render(request, 'img_new.html', {'form': form, 'error': 'Выберите один способ загрузки'})
            if form.cleaned_data['img']:
                img = form.cleaned_data['img']
                width, height = get_image_dimensions(img)
                img = Image.objects.create(img=img, width=width, height=height)
                return redirect('img_view', img_id=img.id)
            if form.cleaned_data['link']:
                url = form.cleaned_data['link']
                response = requests.get(url)
                response.raise_for_status()
                try:
                    img = BytesIO(response.content)
                    PIL.Image.open(img)
                except IOError:
                    return render(request, 'img_new.html', {'form': form, 'error': 'Ссылка не является изображением'})
                filename = url.split('/')[-1]
                with open(f'media/{filename}', 'wb') as file:
                    file.write(response.content)
                width, height = get_image_dimensions(f'media/{filename}')
                img = Image.objects.create(img=filename, width=width, height=height)
                return redirect('img_view', img_id=img.id)
    else:
        form = ImageForm()
        return render(request, 'img_new.html', {'form': form})


def img_view(request, img_id):
    img = get_object_or_404(Image, id=img_id)
    attitude = img.width / img.height
    size = f'{img.width}x{img.height}'
    form = ImgForm(request.POST or None, instance=img)
    if request.method == 'POST' and form.is_valid():
        new_size = form.save(commit=False)
        if form.cleaned_data['height'] and not form.cleaned_data['width']:
            new_size.width = form.cleaned_data['height'] * attitude
        else:
            new_size.height = form.cleaned_data['width'] / attitude
        new_size.save()
        return redirect('img_view', img_id=img.id)
    context = {'form': form, 'image': img, 'size': size}
    return render(request, 'img_view.html', context)
