from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("home")

def products(request):
    return HttpResponse('product')

def customer(request):
    return HttpResponse('Customer')
