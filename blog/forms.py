from django import forms
from .models import Blog

class CreateBlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=('title','description','image','body')
        labels={
            'title':'',
            'description':'',
            'image':'',
            'body':'',
        }
        widgets={
            'title':forms.TextInput(attrs={
                'class':'form-control border-input',
                'placeholder':'Blog Title'}),
            'description':forms.TextInput(attrs={
                'class':'form-control border-input',
                'placeholder':'Blog Description'}),
            'image':forms.FileInput(attrs={
                'class':'form-control border-input',
                'placeholder':'Blog Image'}),
            'body':forms.Textarea(attrs={
                'class':'form-control border-input text-area-resize-disable',
                'placeholder':'Blog Body',
                'rows':'10'}),
        }