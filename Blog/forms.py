from django import forms
from django.forms.models import ModelForm
from .models import Comment, Story

class SearchForm(forms.Form):
    query = forms.CharField()

class EmailPostForm(forms.Form):
    name =  forms.CharField()
    email = forms.EmailField()
    to= forms.EmailField()
    comments= forms.CharField(required=False,widget=forms.Textarea)    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

class StoryForm(forms.ModelForm):
    name =  forms.CharField()
    class Meta:
        model = Story
        fields = '__all__'