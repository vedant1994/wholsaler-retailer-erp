from django import forms
from django.contrib.auth.models import User
from .models import ShopProfile, WholesalerProfile, UserProfile, Stockforwholesaler, Invoice, InvoiceItem, Product

class ShopRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@company.com'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter strong password'})
    )

    class Meta:
        model = ShopProfile
        fields = ['shop_name', 'phone', 'gst_number', 'address']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Apex Retail Store'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 24AAACA12341ZV'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full store address'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def save(self, commit=True):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        shop_profile = super().save(commit=False)
        shop_profile.user = user

        if commit:
            shop_profile.save()
        return shop_profile


class WholesalerRegistrationForm(forms.ModelForm):
        username = forms.CharField(
            max_length=150,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
        )
        email = forms.EmailField(
            widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@company.com'})
        )
        password = forms.CharField(
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter strong password'})
        )
    
        class Meta:
            model = WholesalerProfile
            fields = ['wholesaler_name', 'phone', 'gst_number', 'address']
            widgets = {
                'wholesaler_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Apex Retail Store'}),
                'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'}),
                'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 24AAACA12341ZV'}),
                'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full store address'}),
            }
    
        def clean_username(self):
            username = self.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("This username is already taken. Please choose another.")
            return username
    
        def save(self, commit=True):
            username = self.cleaned_data['username']
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
    
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
    
            wholesaler_profile = super().save(commit=False)
            wholesaler_profile.user = user
    
            if commit:
                wholesaler_profile.save()
            return wholesaler_profile


# Shopekeeper profilecreation from wholesaler
class ShopkeeperCreationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Create shopkeeper username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'shopkeeper@store.com'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter temporary password', 'id': 'shopkeeperPassword'})
    )

    class Meta:
        model = ShopProfile
        fields = ['shop_name', 'phone', 'gst_number', 'address']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Metro Retail Store'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 24AAACA12341ZV'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full shop address'}),
        }


    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

    def save(self, wholesaler, commit=True):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        # Create Django User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            role="SHOPKEEPER"
        )

        # Create ShopProfile
        shop = super().save(commit=False)
        shop.user = user
        shop.wholesaler = wholesaler

        if commit:
            shop.save()

        return shop

class StockForm(forms.ModelForm):
    class Meta:
        model = Stockforwholesaler
        fields = [
            'product_name', 'description', 'product_code', 'category', 'brand', 
            'units_per_box', 'quantity', 'purchase_price', 'selling_price', 
            'mrp_per_unit', 'gst', 'supplier', 'batch_number', 'manufacturing_date', 'expiry_date', 
            'minimum_stock_level', 'warehouse', 'purchase_invoice_number', 'purchase_date'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional description'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. PROD001'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand Name'}),
            'units_per_box': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'No. of boxes'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Purchase Amount'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Selling Amount'}),
            'mrp_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MRP (per unit)'}),
            'gst': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.0'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Name'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'manufacturing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'minimum_stock_level': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'warehouse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Warehouse Name/Location'}),
            'purchase_invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Number'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer_name', 'customer_phone', 'customer_address', 'payment_status']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'payment_status': forms.Select(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], attrs={'class': 'form-select'}),
        }

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'price_per_unit', 'gst_percent', 'discount']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select product-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control item-quantity', 'min': 1}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control item-price', 'step': '0.01', 'min': 0}),
            'gst_percent': forms.NumberInput(attrs={'class': 'form-control item-gst', 'step': '0.01', 'min': 0}),
            'discount': forms.NumberInput(attrs={'class': 'form-control item-discount', 'min': 0}),
        }

InvoiceItemFormSet = forms.inlineformset_factory(
    Invoice, InvoiceItem, form=InvoiceItemForm,
    extra=1, can_delete=True
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'base_price', 'gst_percent', 'stock_quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gst_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
