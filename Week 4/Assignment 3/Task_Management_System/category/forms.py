from django import forms
from .models import TaskCategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory
        fields = ['category_name']

        labels = {
            'category_name': 'Category Name:'
        }