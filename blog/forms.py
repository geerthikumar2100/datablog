from django import forms
from .models import BlogPost
from taggit.forms import TagWidget

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'tags']
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Add tags...'}),
        }
        help_texts = {
            'tags': '', 
        }
