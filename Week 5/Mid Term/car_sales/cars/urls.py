from django.urls import path
from .views import CarListView, CarDetailView, buy_car, add_car, add_brand, home

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('carlist/', CarListView.as_view(), name='car_list'),
    path('<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('<int:pk>/buy/', buy_car, name='buy_car'),
    path('add/', add_car, name='add_car'),
    path('brand/add/', add_brand, name='add_brand'),
]
