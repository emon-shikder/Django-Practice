from django.shortcuts import render, redirect
from .models import TaskModel
from .forms import TaskForm

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_tasks')
    else:
        form = TaskForm()
    return render(request, 'task/add_task.html', {'form': form})

def show_tasks(request):
    tasks = TaskModel.objects.all()
    return render(request, 'task/show_tasks.html', {'tasks': tasks})

def edit_task(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('show_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task/edit_task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    task.delete()
    return redirect('show_tasks')

def complete_task(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    task.is_completed = True
    task.save()
    return redirect('show_tasks')
