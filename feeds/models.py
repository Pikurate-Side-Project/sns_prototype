import re

from django.urls import reverse
from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='feeds/post/%Y/%m/%d')
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.caption
    
    def extract_tag_list(self):
        tag_list = []
        for tag_name in re.findall(r'#([a-zA-Zㄱ-힣]+)', self.caption):
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        
        return tag_list
    
    def get_absolute_url(self):
        return reverse('feeds:post_detail', args=[self.pk])

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name