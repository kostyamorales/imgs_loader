from django import forms
from .models import Image


class ImageForm(forms.Form):
    link = forms.URLField(label='Ссылка', required=False)
    img = forms.ImageField(label='Файл', required=False)


class ImgForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('width', 'height',)
        labels = {
            'width': 'Ширина',
            'height': 'Высота',
        }
