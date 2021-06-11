from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.store, name="store"),
    #path('search/', views.search, name="search"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('faq/', views.faq, name="faq"),
    path('contact/', views.contact, name="contact"),
    path('signup/', views.signUp, name="signup"),
    path('myOrders/', views.myOrders, name="myOrders"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('product/<str:slug>/<int:id>', views.productDetail, name="product_detail"),
    path('product-list/', views.productList, name="product_list"),
    path('product-list/<str:brandCat>/', views.productCategory, name="product_category"),
    path('deepSearch/', views.deepSearch, name="deepSearch"),
    path('adminOrder/', views.adminOrder, name="adminOrder"),

]
