from django.conf import settings
from django.urls import include, path

from . import views

app_name = 'feeds'

urlpatterns = [
    path('post/', views.post_new, name='post'),
    path('detail/<int:pk>/', views.post_detail, name='post_detail'),
]