from django.db import models
from  django.utils import timezone
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User, auth

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default= "")  
    description = models.TextField( default= "")  
    price = models.CharField(max_length=200, default="")
    unit = models.CharField(max_length=200, default="")
    description = models.TextField(default = '')
    status = models.CharField(max_length=200, default="available")
    image = models.ImageField(upload_to="dashboard/images/product",default="")
    def ___str___(self): 
            return self.id

class ProductReviews(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default= "")  
    email = models.CharField(max_length=100, default= "")  
    review = models.TextField( default= "")  
    date = models.CharField(max_length=200, default="")
    def ___str___(self): 
            return self.id


class Subscribe(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, default= "")  
    date = models.CharField(max_length=200, default="")
    def ___str___(self): 
            return self.id

class Dealer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, default= "")  
    password = models.CharField(max_length=100, default= "")
    sponseredId = models.CharField(max_length=200, default= "")
    pins = models.IntegerField(null = True ,default= 10) 
    date = models.DateField(null = True) 

    walletBalance = models.IntegerField(null = True, default =0) 
    paidBalance = models.IntegerField(null = True, default =0) 
    pendingBalance = models.IntegerField(null = True, default =0) 
    
    bankName = models.CharField(max_length=200, default="")
    ifscCode = models.CharField(max_length=200, default="")
    accountNumber = models.CharField(max_length=200, default="")
    status = models.CharField(max_length=200, default="under-review")
    remark = models.CharField(max_length=200, default="")

    def ___str___(self): 
            return self.phone

class Distributor(models.Model):
    id = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    name  = models.CharField(max_length=100, default= "")  
    email  = models.CharField(max_length=100, default= "")  
    phone = models.CharField(max_length=100, default= "")  
    sponseredId = models.CharField(max_length=100, default= "") 
    status = models.CharField(max_length=100, default= "under-review") 
    date = models.DateField(null = True) 

    
    def ___str___(self): 
            return self.id

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    requestAmount = models.IntegerField(null=True, default= 0)  
    paidAmount = models.IntegerField(null=True, default= 0)  
    transactionType = models.CharField(max_length= 300, default= "Credit")
    transactionMode = models.CharField(max_length= 300, default= "")
    requestDate = models.DateField(null= True)
    paidDate = models.DateField(null= True)
    status = models.CharField(max_length=200, default="unpaid")

    def ___str___(self): 
            return self.id           

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    productName = models.TextField(default="", null= True)
    amount = models.IntegerField(null=True, default= 0)  
    phone = models.CharField(max_length=200, default="", null= True)
    name = models.CharField(max_length=200, default="", null= True)
    qnt = models.CharField(max_length=200, default="", null= True)
    email = models.CharField(max_length=200, default="", null= True)
    city = models.CharField(max_length=200, default="", null= True)
    pincode = models.CharField(max_length=200, default="", null= True)
    address = models.TextField(default="", null= True)
    msg = models.TextField(default="", null= True)
    
    transactionType = models.CharField(max_length= 300, default= "")
    order_id = models.CharField(max_length= 300, default= "")
    transactionMode = models.CharField(max_length= 300, default= "")
    paymentId = models.CharField(max_length= 300, default= "")
    date = models.DateField(null= True)

    status = models.CharField(max_length=200, default="")

    def ___str___(self): 
            return self.id           

class Inbox(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length= 200, default= "")
    phone = models.CharField(max_length= 200, default= "")
    name = models.CharField(max_length= 200, default= "")
    
    subject = models.CharField(max_length= 300, default= "")
    msg = models.CharField(max_length= 500, default= "")
    date = models.DateField(null= True)
    status = models.CharField(max_length=200, default="new")

    def ___str___(self): 
            return self.id           

class AdminNotifications(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length= 100, default= "")
    msg = models.CharField(max_length= 500, default= "")
    date = models.DateTimeField(null= True)
    link = models.CharField(max_length=200, default="")

    def ___str___(self): 
            return self.id           

class UserNotifications(models.Model):
    id = models.AutoField(primary_key=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    status = models.CharField(max_length= 100, default= "new")
    msg = models.CharField(max_length= 500, default= "")
    date = models.DateTimeField(null= True)
    link = models.CharField(max_length=200, default="")

    def ___str___(self): 
            return self.id           


