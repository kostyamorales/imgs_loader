from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('img_new', views.img_new, name='img_new'),
    path('imgs/<int:img_id>/', views.img_view, name='img_view'),
]
