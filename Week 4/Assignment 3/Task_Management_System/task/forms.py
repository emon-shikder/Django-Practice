from django import forms
from .models import TaskModel

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['taskTitle', 'taskDescription', 'is_completed', 'categories']
        
        labels = {
            'taskTitle': 'Enter your Task Title',
            'taskDescription': 'Description',
            'is_completed': 'Your Task is Completed?',
            'categories': 'Categories:'
        }

        widgets ={
            'categories': forms.CheckboxSelectMultiple(),
        }