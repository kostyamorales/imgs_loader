from django.contrib import admin

from img_resize.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'width', 'height',)
