from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('verify/', views.verify_invoice, name='verify_invoice'),
    path('verify/<str:invoice_number>/', views.verify_invoice, name='verify_invoice_num'),
    path('contact/', views.contact, name='contact'),
    
    path('register/', views.register_select, name='register'),
    path('register/wholesaler/', views.register_wholesaler, name='register_wholesaler'),
    path('register/shopkeeper/', views.register_shopkeeper, name='register_shopkeeper'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("create-shopkeeper/",views.create_shopkeeper,name="create_shopkeeper"),
    path("retailers/", views.retailer_list, name="retailer_list"),
    path("stock/", views.stock_list, name="stock_list"),
    path("stock/add/", views.add_stock, name="add_stock"),
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.add_product, name="add_product"),
    path("invoice/create/", views.create_invoice, name="create_invoice"),
    path("invoice/history/", views.invoice_history, name="invoice_history"),
]
