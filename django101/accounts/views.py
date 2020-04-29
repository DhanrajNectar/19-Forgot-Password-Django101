from cgi import log
from logging import log

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def home(request):

    return render(request, 'accounts/home.html')

def products(request):
    return render(request, 'accounts/products.html')

def customer(request):
    return render(request, 'accounts/customer.html')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')