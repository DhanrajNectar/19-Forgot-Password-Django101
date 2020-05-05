from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .forms import OrderForm, CreateUserForm
from .models import *
from .filters import OrderFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



def registerPage(request):
    if request.user.is_authenticated:
        return redirect('')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('dashboard')
        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# Create your views here.
def home(request):
    return render(request, 'accounts/home.html')

@login_required()
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required()
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)  # ambil customer berdasarkan id
    orders = customer.order_set.all()  # ambil order berdasarkan customer
    order_count = orders.count()  # menghitung jumlah orderan tiap customer

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilter': myFilter
               }
    return render(request, 'accounts/customer.html', context)

@login_required
def dashboard(request):
    customers = Customer.objects.all()
    total_customer = customers.count()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()

    context = {
        'customers': customers,
        'orders': orders,
        'total_orders': total_orders,
        'total_customer': total_customer,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
