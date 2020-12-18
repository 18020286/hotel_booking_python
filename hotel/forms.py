from django.forms import ModelForm
from .models import Room, Blog


class CategoryForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'