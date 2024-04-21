from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.functions import RowNumber
import time


STATUS = ((0, "Draft"), (1, "Published"))


class Thing(models.Model):
    '''Django database model for a Thing or a Component of the diy things '''
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='components')
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey( User, on_delete=models.CASCADE, related_name="owner")
    featured_image = CloudinaryField('image', default='placeholder')
    description = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='thing_likes', blank=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

class Instructions(models.Model):
    '''Django database model for Instructions of the diy things '''
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name="instructions")

    def default_Instruction_title():
        now=time.localtime()
        return f"I-{now.tm_year}-{now.tm_mon}-{now.tm_mday}_{now.tm_hour}:{now.tm_min}:{now.tm_sec}"
    title = models.CharField(max_length=200, default=default_Instruction_title)
    instructions = models.TextField( blank=True, null=False)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return str(self.title)
