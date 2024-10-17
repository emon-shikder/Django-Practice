from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import UserBankAccount
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'