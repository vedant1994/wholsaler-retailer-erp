from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import ShopRegistrationForm, WholesalerRegistrationForm, ShopkeeperCreationForm, StockForm
from .models import WholesalerProfile, Invoice, Product, Stockforwholesaler

def home(request):
    return render(request, "invoices/home.html")

def about(request):
    return render(request, "invoices/about.html")

def features(request):
    return render(request, "invoices/features.html")

def verify_invoice(request, invoice_number=None):
    query = invoice_number or request.GET.get("inv", "").strip()
    invoice = None
    if query:
        invoice = Invoice.objects.filter(Invoice_number=query).first()

    return render(request, "invoices/verify_invoice.html", {
        "query": query,
        "invoice": invoice,
    })

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        messages.success(request, f"Thank you {name}! Your message has been received. Our support team will get back to you shortly.")
        return redirect("invoices:contact")
    return render(request, "invoices/contact.html")


# Registration Selection View
def register_select(request):
    if request.user.is_authenticated:
        return redirect("invoices:dashboard")
    return render(request, "registration/register_select.html")

# Alias for backward compatibility
register = register_select

# Shopkeeper Register form
def register_shopkeeper(request):
    if request.user.is_authenticated:
        return redirect("invoices:dashboard")

    if request.method == "POST":
        form = ShopRegistrationForm(request.POST)
        if form.is_valid():
            shop_profile = form.save()
            login(request, shop_profile.user)
            messages.success(
                request,
                f"Welcome {shop_profile.shop_name}! Your shop registration was successful."
            )
            return redirect("invoices:login")
    else:
        form = ShopRegistrationForm()

    return render(request, "registration/register_shopkeeper.html", {"form": form})

# Wholesaler Register form
def register_wholesaler(request):
    if request.user.is_authenticated:
        return redirect("invoices:dashboard")

    if request.method == "POST":
        form = WholesalerRegistrationForm(request.POST)
        if form.is_valid():
            wholesaler_profile = form.save()
            login(request, wholesaler_profile.user)
            messages.success(
                request,
                f"Welcome {wholesaler_profile.wholesaler_name}! Your wholesaler registration was successful."
            )
            return redirect("invoices:login")
    else:
        form = WholesalerRegistrationForm()

    return render(request, "registration/register_wholesaler.html", {"form": form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect("invoices:dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("invoices:dashboard")
        else:
            messages.error(request, "Invalid username or password. Please check your credentials.")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("invoices:login")

@login_required
def dashboard(request):
    user = request.user
    
    # Try to get ShopProfile first
    if hasattr(user, 'shopprofile'):
        shop = user.shopprofile
        invoices = Invoice.objects.filter(shop=shop).order_by('-created_at')
        total_invoices = invoices.count()
        context = {
            "shop": shop,
            "role": "shopkeeper",
            "total_invoices": total_invoices,
            "invoices": invoices,
        }
        return render(request, "invoices/dashboard.html", context)
        
    # Otherwise check for WholesalerProfile
    elif hasattr(user, 'wholesalerprofile'):
        wholesaler = user.wholesalerprofile
        # Wholesalers might want to see all invoices from their shops
        # or maybe just their own dashboard
        shops = wholesaler.shops.all()
        invoices = Invoice.objects.filter(shop__in=shops).order_by('-created_at')
        total_invoices = invoices.count()
        context = {
            "wholesaler": wholesaler,
            "role": "wholesaler",
            "shops": shops,
            "total_invoices": total_invoices,
            "invoices": invoices,
        }
        return render(request, "invoices/dashboard.html", context)
        
    else:
        # Fallback if the user has neither profile (e.g. superuser)
        messages.error(request, "You do not have a registered Shop or Wholesaler profile.")
        return redirect("invoices:home")

@login_required
def create_shopkeeper(request):
    if not hasattr(request.user, 'wholesalerprofile'):
        messages.error(request, "Only wholesalers can create shopkeeper accounts.")
        return redirect("invoices:dashboard")

    wholesaler = request.user.wholesalerprofile

    if request.method == "POST":
        form = ShopkeeperCreationForm(request.POST)
        if form.is_valid():
            shop = form.save(wholesaler=wholesaler)
            messages.success(request, f"Shopkeeper account for '{shop.shop_name}' created successfully.")
            return redirect("invoices:dashboard")
    else: 
        form = ShopkeeperCreationForm()

    return render(
        request, "invoices/create_shopkeeper.html", {
            "form": form,
            "wholesaler": wholesaler
        }
    )

@login_required
def retailer_list(request):
    if not hasattr(request.user, 'wholesalerprofile'):
        messages.error(request, "Only wholesalers can view the retailer list.")
        return redirect("invoices:dashboard")

    wholesaler = request.user.wholesalerprofile
    shops = wholesaler.shops.all()

    return render(
        request, "invoices/retailer_list.html", {
            "wholesaler": wholesaler,
            "shops": shops
        }
    )

@login_required
def stock_list(request):
    if not hasattr(request.user, 'wholesalerprofile'):
        messages.error(request, "Only wholesalers can view the stock list.")
        return redirect("invoices:dashboard")

    wholesaler = request.user.wholesalerprofile
    stocks = Stockforwholesaler.objects.filter(wholesaler=wholesaler)

    return render(
        request, "invoices/stock_list.html", {
            "wholesaler": wholesaler,
            "stocks": stocks
        }
    )

@login_required
def add_stock(request):
    if not hasattr(request.user, 'wholesalerprofile'):
        messages.error(request, "Only wholesalers can add stock.")
        return redirect("invoices:dashboard")

    wholesaler = request.user.wholesalerprofile

    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.wholesaler = wholesaler
            stock.save()
            messages.success(request, f"Product '{stock.product_name}' added to inventory successfully.")
            return redirect("invoices:stock_list")
    else: 
        form = StockForm()

    return render(
        request, "invoices/add_stock.html", {
            "form": form,
        }
    )
