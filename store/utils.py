import json
from .models import *
from django.core.exceptions import MultipleObjectsReturned

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': True}
    cartItems = order['get_cart_items']

    for i in cart:
        try:    
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)

            total = (product.price * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'brand':product.brand,
                    'slug':product.slug,
                    'detail':product.detail,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total,
            }
            items.append(item)

        except:
            pass
            
    return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]

    return { 'cartItems':cartItems, 'order':order, 'items':items}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
            email=email,
            )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
        )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
        )
    return customer, order


def getUserData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer, complete=True)
        print(orders)
        print(len(orders))
        try:
            orderItems = []
            for i in range(len(orders)):
                items = OrderItem.objects.filter(order=orders[i])
                for j in range(len(items)):
                    orderItems.append(items[j])
                    print(items[j])

        except (MultipleObjectsReturned):
            pass

    return {'customer':customer, 'orders':orders, 'orderItems': orderItems}