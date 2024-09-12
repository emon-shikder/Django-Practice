from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Car, Brand, Comment
from orders.models import Order
from django.contrib.auth.decorators import login_required
from .forms import CarForm, BrandForm
from .forms import CommentForm
from django.contrib import messages

@login_required
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = BrandForm()
    return render(request, 'cars/brand_form.html', {'form': form})

@login_required
def add_car(request):
    """View to handle adding a new car."""
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car added successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Error adding car. Please correct the errors below.')
    else:
        form = CarForm()
    return render(request, 'cars/car_form.html', {'form': form})

class CarListView(ListView):
    model = Car
    template_name = 'home.html'
    context_object_name = 'cars'

    def get_queryset(self):
        brand_name = self.request.GET.get('brand')
        if brand_name:
            return Car.objects.filter(brand__name=brand_name)
        return Car.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        return context


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = self.object
            comment.save()
        return redirect('car_detail', pk=self.object.pk)

@login_required
def buy_car(request, pk):
    car = Car.objects.get(pk=pk)
    if car.quantity > 0:
        car.quantity -= 1
        car.save()
        Order.objects.create(user=request.user, car=car)
        return redirect('profile')
    return redirect('car_list')

def home(request):
    brands = Brand.objects.all()
    brand_name = request.GET.get('brand')
    if brand_name:
        cars = Car.objects.filter(brand__name=brand_name)
    else:
        cars = Car.objects.all()

    context = {
        'brands': brands,
        'cars': cars,
    }
    return render(request, 'cars//home.html', context)