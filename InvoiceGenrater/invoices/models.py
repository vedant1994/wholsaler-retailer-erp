from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICE=[
        ("WHOLESALER","wholesaler"),
        ("SHOPKEEPER","shopekeeper"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role=models.CharField(
        max_length=20,
        choices=ROLE_CHOICE
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class WholesalerProfile(models.Model):
    APPROVAL_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wholesaler_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default="APPROVED",
    )
    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return self.wholesaler_name

class ShopProfile(models.Model):
    APPROVAL_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    wholesaler = models.ForeignKey(
        WholesalerProfile,
        on_delete=models.SET_NULL,
        related_name="shops",
        null=True,
        blank=True
    )

    shop_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    address = models.TextField()

    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default="APPROVED",
    )

    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return self.shop_name

class Stockforwholesaler(models.Model):
    wholesaler = models.ForeignKey(WholesalerProfile, on_delete=models.CASCADE, related_name="stocks", null=True, blank=True)
    product_name = models.CharField(max_length=40)
    description = models.CharField(max_length=40, null=True, blank=True)
    product_code = models.CharField(max_length=30)
    category = models.CharField(max_length=40)
    brand = models.CharField(max_length=40)
    units_per_box = models.IntegerField()
    total_units = models.IntegerField(null=True, blank=True)
    purchase_price_per_unit = models.FloatField(null=True, blank=True)
    selling_price_per_unit = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField()  # this is the initial quantity of boxes
    purchase_price = models.IntegerField()
    selling_price = models.IntegerField()   
    mrp_per_unit = models.IntegerField()
    gst = models.FloatField()
    supplier = models.CharField(max_length=40)
    batch_number = models.CharField(max_length=40)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField()
    minimum_stock_level = models.IntegerField()
    warehouse  = models.CharField(max_length=40, null=True, blank=True)
    purchase_invoice_number  = models.CharField(max_length=40, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.quantity is not None and self.units_per_box is not None:
            self.total_units = self.quantity * self.units_per_box
        else:
            self.total_units = 0
            
        if self.purchase_price is not None and self.total_units > 0:
            self.purchase_price_per_unit = round(self.purchase_price / self.total_units, 2)
        else:
            self.purchase_price_per_unit = 0
            
        if self.selling_price is not None and self.total_units > 0:
            self.selling_price_per_unit = round(self.selling_price / self.total_units, 2)
        else:
            self.selling_price_per_unit = 0
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name

# class Stockorder(models.Model):

class Product(models.Model):
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE)
    Invoice_number = models.CharField(max_length=30, unique=True)
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=15, blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='Unpaid')
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Invoice_number

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.invoice.Invoice_number} - {self.product.name if self.product else 'Item'}"