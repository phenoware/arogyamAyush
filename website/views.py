from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.db.models import Count, F, Value, Q
from django.db.models.functions import Length, Upper
import datetime
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail
from dashboard.models import Product, Order, ProductReviews, Subscribe

from django.contrib.auth import logout  
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf

import random
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
import hashlib
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
from django.conf import settings
from django.core.mail import send_mail
from pattiMallProj import Checksum
import random
import requests
import json
# import PaytmChecksum
import datetime

# Live Mode 
PAYTM_MID = "rgtegE95966529272713"
PAYTM_MERCHANT_KEY = "_gSaAP3E2yOTeXIm"
PAYTM_ENVIRONMENT= 'https://securegw.paytm.in'
PAYTM_WEBSITE= 'DEFAULT'

# test mode 
# PAYTM_MID = "yvPcEZ90289852432461"
# PAYTM_MERCHANT_KEY = "q0L8EcHMSuXTO5K8"
# PAYTM_ENVIRONMENT= 'https://securegw-stage.paytm.in'
PAYTM_WEBSITE= 'WEBSTAGING'


# Email Templates.

def emailTemplate(request):
    return render(request, "app/new-account-mail.html")

# Paytm Payment gateway Integration

def paytmweb(request):

    if request.POST['product'] == '0':
        return HttpResponse("Please select product")
    else :
        product = Product.objects.get(id  = request.POST['product'])
        qnt = int(request.POST['qnt'])
        amount= int(product.price) * qnt
        # amount= str(1)
        productName = product.name
    
    
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    city = request.POST['city']
    pincode = request.POST['pincode']
    address =  request.POST['address']
    qnt = request.POST['qnt']
    msg = request.POST['msg']

    order_id='order_'+str(datetime.datetime.now().timestamp())
    custId = request.POST['email']

    
    # Add Oder In Database 
    order = Order(productName = productName, amount= amount, phone= phone, name = name , email= email, transactionType = 'Online', transactionMode = 'Online', date = datetime.datetime.now(), status = 'Payment Pending' , qnt = qnt, city = city, address = address, pincode = pincode,  msg = msg, order_id = order_id)
    order.save()
    

    # Payment gateway integration 
    paytmParams = dict() 
    paytmParams["body"] = {
        "requestType"   : "Payment",
        "mid"           : PAYTM_MID,
        "websiteName"   : PAYTM_WEBSITE,
        "orderId"       : order_id,
        "callbackUrl"   : "https://arogyamayush.com/handlerequestweb/",
        "txnAmount"     : {
            "value"     : str(amount),
            "currency"  : "INR",
        },
        "userInfo"      : {
            "custId"    : custId,
        },
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = Checksum.generateSignature(json.dumps(paytmParams["body"]), PAYTM_MERCHANT_KEY)

    paytmParams["head"] = {
        "signature"    : checksum
    }

    post_data = json.dumps(paytmParams)

    url = PAYTM_ENVIRONMENT+"/theia/api/v1/initiateTransaction?mid="+PAYTM_MID+"&orderId="+order_id

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    response_str = json.dumps(response)
    res = json.loads(response_str)
    if res["body"]["resultInfo"]["resultStatus"]=='S':
        token=res["body"]["txnToken"]
    else:
        token=""


    dataParams = {'mid':PAYTM_MID, 'amount':str(amount), 'orderid':order_id, 'env':PAYTM_ENVIRONMENT, 'token':token}
    return render(request, 'website/index1.html', dataParams)



@csrf_exempt
def handlerequestweb(request):

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]


    verify = Checksum.verifySignature(response_dict, PAYTM_MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            transaction_id = response_dict['BANKTXNID']
            order_id = response_dict['ORDERID']
            
            order = Order.objects.get(order_id = order_id)
            order.status = 'Order Placed'
            order.save()


            print('order successful')
            # Mail For Admin
            subject = 'New order from Arogyam Ayush website'
            message = f'Dear Sir,\n\nYou have received new order from website as below \nCustomer name : {order.name} ,\nPhone : {order.phone} ,\nAddress : {order.address} ,\nCity : {order.city} ,\nProduct name : {order.productName} ,\nQauntity : {order.qnt},\nAmount : {order.amount}.\n\n{order.msg}'
                
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['arogyamayushhelp@gmail.com']
            send_mail( subject, message, email_from, recipient_list )
            

            # Mail for customer 
            subject = 'Order placed successfully - Arogyam Ayush'
            message = f'Dear Sir,\nCongratilations,  \n\nYour order placed successfully , We will contact you shortly.\nProducts Name :{order.productName},\nQauntity : {order.qnt},\nAmount : {order.amount}.\n\nThanking you\nTeam Arogyam Ayush'
                
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [order.email]
            send_mail( subject, message, email_from, recipient_list )

            return redirect('/order-placed/')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'website/paymentStatus.html', {'response': response_dict})


def paymentSuccessWeb(request,successPaymentId):
   
    

    # Mail For Admin
    subject = 'New order from Arogyam Ayush website'
    message = f'Dear Sir,\n\nYou have received new order from website as below \nCustomer name : {name} ,\nPhone : {phone} ,\nAddress : {address} ,\nCity : {city} ,\nProduct name : {productName} ,\nQauntity : {qnt},\n\n{msg}'
        
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['arogyamayushhelp@gmail.com']
    send_mail( subject, message, email_from, recipient_list )
    

    # Mail for customer 
    subject = 'Order placed successfully - Arogyam Ayush'
    message = f'Dear Sir,\nCongratilations,  \n\nYour order placed successfully , We will contact you shortly.\nProducts Name :{productName},\nQauntity : {qnt}\n\nThanking you\nTeam Arogyam Ayush'
        
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )

    return redirect('/order-placed/')
    
def orderPlaced(request):
    return render(request, 'website/order-success.html')

def home(request):
    products = Product.objects.all().order_by('-id')
    reviews = ProductReviews.objects.all().order_by('-id')

    params = {'products':products, 'reviews':reviews}
    return render(request, 'website/index.html', params)

def shop(request):
    products = Product.objects.all().order_by('-id')
    productsCount = Product.objects.all().count()

    params = {'products':products, 'productsCount':productsCount}
    return render(request, 'website/shop.html', params)

# Products Managenet 
def productDetails(request, id):
    redirectUrl = request.GET.get('redirectUrl')
    product = Product.objects.get(id = id)
    products = Product.objects.all().order_by('-id')
    reviews = ProductReviews.objects.filter(product_id = id).order_by('-id')
    reviewsCount = ProductReviews.objects.filter(product_id = id).count()

    params = {'redirectUrl':redirectUrl , 'product':product, 'reviews':reviews, 'reviewsCount':reviewsCount, 'products':products}
    return render(request, 'website/product-details.html', params )


# Review
def submitReview(request):
    if request.method == 'POST':
        redirectUrl = request.GET.get('redirectUrl')
        product = Product.objects.get(id = request.POST['product'])
        name = request.POST['name'] 
        email = request.POST['email'] 
        review = request.POST['review'] 
        date = datetime.datetime.now() 

        ProductReviews(product = product, name= name, email= email, review = review, date= date).save()

        return redirect(''+redirectUrl)
    return redirect('/')


def subsribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        redirectUrl = request.GET.get('redirectUrl')

        Subscribe(email = email , date = datetime.datetime.now()).save()
        messages.success(request,'Thanks for showing your interest !')
        return redirect(''+redirectUrl)

    return redirect('/')

def aboutUs(request):
    return render(request,'website/about-us.html')

def contact(request):
    return render(request, 'website/contact.html')

def sendMessage(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone= request.POST['phone']
        email = request.POST['email']
        userSubject = request.POST['subject']
        msg = request.POST['msg']

        # Send Mail TO Customer
        subject = 'Thanks for connecting with us. - Arogyam Ayush.'
        message = f'Thank you for showing your interest, \n\nWe have received your message, We will contact you very shortly.\n\nThank & Regards\nSales & Support - Arogyam Ayush. '
            
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail( subject, message, email_from, recipient_list )
        print('Mail sent to customer')

        # send mail to admin 

        message = f'Dear Sir, \nWe have received new meesage from arogyam ayush website as below.\n\nName :{name}\nPhone :{phone}\nEmail :{email}\n\nSubject : {userSubject}\nMessage : {msg}'
            
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['arogyamayushhelp@gmail.com']
        send_mail( 'New Message received - Arogyam Ayush.', message, email_from, recipient_list )
        print('Mail sent to admin')

        messages.success(request, 'messag')
        return redirect('/contact/')

    return redirect('/')

def termServices(request):
    app = 1
    params = {'app': app}
    return render(request,'website/term.html',params)

def refundPolicy(request):
    app = 1
    params = {'app': app}
    return render(request,'website/refund.html',params)

def privacyPolicy(request):
    app = 1
    params = {'app': app}
    return render(request,'website/privacy.html',params)


def uploadApk(request):
    return render(request, 'website/upload-apk.html')

def makeUpload(request):
    apk = request.FILES['file']
    date = datetime.datetime.now()
    newApk = APKFile(apk = apk, date= date)
    newApk.save()
    return redirect('/')


def checkout(request):
    if request.method == 'POST':
        redirectUrl = request.GET.get('redirectUrl')
        qnt = request.POST['qnt'] 
        product = Product.objects.get(id = request.POST['product'])

        amount = int(qnt) * int(product.price)

        params = {'qnt':qnt, 'product':product, 'amount':amount, 'redirectUrl':redirectUrl}
        return render(request, 'website/checkout.html', params)

    return redirect('/')

def placeOrder(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    city = request.POST['city']
    address = request.POST['address']
    product = request.POST['product']
    qnt = request.POST['qnt']
    msg = request.POST['msg']

    # Mail for admin 
    subject = 'New order from 52 Patti Mall website'
    message = f'Dear Sir,\n\nYou have received new order from website as below \nCustomer name : '+name+' ,\nPhone : '+phone+' ,\nAddress : '+address+' ,\nCity : '+city+' ,\nProduct name : '+product+' ,\nQauntity : '+str(qnt)+',\n\n'+msg
        
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['inwmarathi@gmail.com']
    send_mail( subject, message, email_from, recipient_list )
    

    # Mail for customer 
    subject = 'Order placed successfully - 52 Patti Mall'
    message = f'Dear Sir,\nCongratilations,  \n\nYour order placed successfully , We will contact you shortly.\n\nThanking you\nTeam 52 Patti Mall'
        
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
    return render(request, 'website/order-success.html')

def resultPanel(request):
    markets = Market.objects.all()
    params = {'markets': markets }
    return render(request, 'website/result-panel.html', params)


def resultPanelChart(request, id):
    market = Market.objects.get(id= id)
    marketName = market.title
    chart = PanelChartRegulerMarket.objects.filter(market_id = id)
    params = {'chart': chart, 'marketName':marketName }
    return render(request, 'website/result-panel-chart.html', params)