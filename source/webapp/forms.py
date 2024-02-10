from django import forms

from .models import *


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['image', 'title', 'description', 'author', 'category', 'price', 'status']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'author', 'announcement']
