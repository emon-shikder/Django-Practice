# cars/forms.py

from django import forms
from .models import Car, Brand, Comment

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter brand name'}),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'title', 'description', 'price', 'quantity', 'image']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter car title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter car description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter car price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter car quantity'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your comment'}),
        }