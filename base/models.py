from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    name=models.CharField( max_length=150,blank=True,null=True)
    image = models.ImageField(null=True, blank=True,default='/placeholder.png')
    brand=models.CharField( max_length=150,blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    rating=models.DecimalField( max_digits=7, decimal_places=2,blank=True,null=True)    
    price=models.DecimalField( max_digits=7, decimal_places=2,blank=True,null=True)
    numReviews=models.IntegerField(blank=True,null=True ,default=0)    
    countInStock=models.IntegerField(blank=True,null=True ,default=0)
    createdAt=models.DateTimeField( auto_now_add=True)
    _id=models.AutoField(primary_key=True,editable=False)
    category = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    name=models.CharField( max_length=150,blank=True,null=True)
    rating=models.IntegerField(blank=True,null=True ,default=0)
    comment=models.TextField(blank=True,null=True)
    createdAt=models.DateTimeField(auto_now_add=True)
    _id=models.AutoField(primary_key=True,editable=False)


    def __str__(self):
        return str(self.user.first_name)+"  rated product "+str(self.product.name)+" "+str(self.rating)+" stars"
    
class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    paymentMethod=models.CharField( max_length=150,blank=True,null=True)
    taxPrice=models.DecimalField( max_digits=7, decimal_places=2,blank=True,null=True)
    shippingPrice=models.DecimalField( max_digits=7, decimal_places=2,blank=True,null=True)
    totalPrice=models.DecimalField( max_digits=7, decimal_places=2,blank=True,null=True)
    isPaid=models.BooleanField(default=False)
    isDelivered=models.BooleanField(default=False)
    paidAt=models.DateTimeField(blank=True,null=True, auto_now_add=False)
    deliverdAt=models.DateTimeField(blank=True,null=True, auto_now_add=False)
    createdAt=models.DateTimeField( auto_now_add=True)
    _id=models.AutoField(primary_key=True,editable=False)
    def __str__(self):
        return str(self.createdAt)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)
    
