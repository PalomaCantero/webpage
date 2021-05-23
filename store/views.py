from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from .forms import *
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

# Create your views here.

def store(request):
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render (request, 'store/store.html', context)

def faq(request):
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {'cartItems':cartItems}
    return render (request, 'store/faq.html', context)

def cart(request):
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render (request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render (request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

def contact(request):
    data = cartData(request)
    cartItems = data["cartItems"]

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry" 
            body = {
            'first_name': form.cleaned_data['first_name'], 
            'last_name': form.cleaned_data['last_name'], 
            'email': form.cleaned_data['email_address'], 
            'message':form.cleaned_data['message'], 
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect ("store")
      
    form = ContactForm()
    return render(request, "store/contact.html", {'form':form, 'cartItems':cartItems})

def signUp(request):
    data = cartData(request)
    cartItems = data["cartItems"]

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        customer_form = RegistrationForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            login(request, user)
            return redirect('store')
    else:
        user_form = UserCreationForm()
        customer_form = RegistrationForm()
    return render(
        request,
        'store/signup.html',
        {'user_form': user_form, 'customer_form': customer_form, 'cartItems':cartItems}
    )

def productDetail(request, slug, id):
    data = cartData(request)
    cartItems = data["cartItems"]

    product = Product.objects.get(id=id)
    return render(request, 'store/productdetail.html', {'product':product, 'cartItems':cartItems})