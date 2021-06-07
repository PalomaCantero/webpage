from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse,resolve
from store.views import *
from store.models import Customer, Order, Brand, Product
from django.contrib.auth.models import User
import datetime


class TestUrls (SimpleTestCase):

    def test_store_url_resolves(self):
        url = reverse('store')
        self.assertEquals(resolve(url).func, store)


    def test_cart_url_resolves(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func, cart)


    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, checkout)


    def test_updateItem_url_resolves(self):
        url = reverse('update_item')
        self.assertEquals(resolve(url).func, updateItem)


    def test_processOrder_url_resolves(self):
        url = reverse('process_order')
        self.assertEquals(resolve(url).func, processOrder)


    def test_faq_url_resolves(self):
        url = reverse('faq')
        self.assertEquals(resolve(url).func, faq)

    def test_contact_url_resolves(self):
        url = reverse('contact')
        self.assertEquals(resolve(url).func, contact)

    def test_signUp_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signUp)

    def test_myOrders_url_resolves(self):
        url = reverse('myOrders')
        self.assertEquals(resolve(url).func, myOrders)


class TestViews(TestCase):

    def setUp (self):
        self.client = Client()

    # GET METHODS
    def test_store_GET(self):        
        response = self.client.get(reverse('store'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

    #To check it performs correctly: (It throws an error)
    def test_store_GET(self):
        client = Client()
        
        response = client.get(reverse('store'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'store/store.htmls')


    def test_faq_GET(self):        
        response = self.client.get(reverse('faq'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/faq.html')

    def test_cart_GET(self):        
        response = self.client.get(reverse('cart'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')

    def test_contact_GET(self):        
        response = self.client.get(reverse('contact'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/contact.html')

    def test_signUp_GET(self):        
        response = self.client.get(reverse('signup'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/signup.html')


# TEST MODELS
class TestModels(TestCase):

    def setUp (self):
        self.client = Client()

    def test_product_ADD(self):

        brand1 = Brand.objects.create(
            name='Nike'
        )

        product1 = Product.objects.create(
            name = 'Continental80',
            slug = '/Continental80/',
            detail = 'Pretty',
            brand = brand1,
            price = 89.99,

        )

        self.assertEquals(Product.objects.count(), 1)
        self.assertEquals(str(product1), 'Continental80')

    def test_customer_ADD(self):

        user1 = User.objects.create(
            
        )

        self.customer = Customer.objects.create(
            user = user1,
            name = 'Luis',
            email = 'pinillarubioluis@gmail.com',
            mobile = '622854876',
            registerDate = datetime.datetime.now()
        )

        self.assertEquals(str(self.customer), "Luis")
        self.assertEquals(Customer.objects.count(), 1)

    def test_brand_ADD(self):
        brand1 = Brand.objects.create(
            name='Nike'
        )
        self.assertEquals(str(brand1), "Nike")
        self.assertEquals(Brand.objects.count(), 1)


    def test_order_ADD(self):
        user1 = User.objects.create(
            
        )

        customer1 = Customer.objects.create(
            user = user1,
            name = 'Luis',
            email = 'pinillarubioluis@gmail.com',
            mobile = '622854876',
            registerDate = datetime.datetime.now()
        )

        order1 = Order.objects.create(

            customer = customer1,
            transaction_id = 19028928,
            date_ordered = datetime.datetime.now(),
            complete = False
        )
        self.assertEquals(str(order1), '1')
        self.assertEquals(Order.objects.count(), 1)


    def test_shippingAddress_ADD(self):

        user1 = User.objects.create(
            
        )

        customer1 = Customer.objects.create(
            user = user1,
            name = 'Luis',
            email = 'pinillarubioluis@gmail.com',
            mobile = '622854876',
            registerDate = datetime.datetime.now()
        )
                
        order1 = Order.objects.create(

            customer = customer1,
            transaction_id = 19028928,
            date_ordered = datetime.datetime.now(),
            complete = False
        )

        shippingAddress1 = ShippingAddress.objects.create(
            customer = customer1,
            address = 'Boleslawa Prusa 9',
            city = 'Wroclaw',
            state = 'Wroclaw',
            zipcode = 50319,
            date_added = datetime.datetime.now(),
            order = order1
        )

        self.assertEquals(str(shippingAddress1), 'Boleslawa Prusa 9')
        self.assertEquals(ShippingAddress.objects.count(), 1)


    def test_orderItem_ADD(self):

        user1 = User.objects.create(
            
        )

        customer1 = Customer.objects.create(
            user = user1,
            name = 'Luis',
            email = 'pinillarubioluis@gmail.com',
            mobile = '622854876',
            registerDate = datetime.datetime.now()
        )
                
        order1 = Order.objects.create(

            customer = customer1,
            transaction_id = 19028928,
            date_ordered = datetime.datetime.now(),
            complete = False
        )

        brand1 = Brand.objects.create(
            name='Nike'
        )

        product1 = Product.objects.create(
            name = 'Continental80',
            slug = '/Continental80/',
            detail = 'Pretty',
            brand = brand1,
            price = 90,
        )
        orderItem1 = OrderItem.objects.create(
            order = order1,
            product = product1,
            quantity = 4,
            date_added = datetime.datetime.now()
        )  

        self.assertEquals(orderItem1.get_total, 360)
        self.assertEquals(OrderItem.objects.count(), 1)
        self.assertEquals(order1.get_cart_total, 360)
        self.assertEquals(order1.get_cart_items, 4)
