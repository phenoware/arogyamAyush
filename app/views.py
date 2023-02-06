# from django.shortcuts import render,redirect
# from django.http import HttpResponse
# from django.template import loader
# from django.contrib.auth.models import User, auth
# from django.contrib.auth import authenticate, login,logout
# from dashboard.models import Market, JodiMarket, Games, Customer, BiddingHistory, JodiBiddingHistory, Withdraw, Transaction, Notifications,BankAccount, Partner, PartnerUser, PartnerWithdraw, PanelChartRegulerMarket , PanelChartJodiMarket, UserRoll, Card
# from django.contrib import messages
# from django.db.models import Count, F, Value
# from django.db.models.functions import Length, Upper
# import datetime
# import http.client
# import razorpay
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.contrib.auth import logout  
# from django.utils import timezone
# from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from django.template.context_processors import csrf

# import random
# from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from django.template.context_processors import csrf
# import hashlib
# from django.template.loader import get_template
# from django.template import Context, Template,RequestContext
# from django.conf import settings
# from django.core.mail import send_mail
# from pattiMallProj import Checksum
# import random
# import requests
# import json
# # import PaytmChecksum
# import datetime

# PAYTM_MID = "wdRVdJ51632956452397"
# PAYTM_MERCHANT_KEY = "jJ819wGiAlcp1eH0"
# PAYTM_ENVIRONMENT= 'https://securegw.paytm.in'
# PAYTM_WEBSITE= 'DEFAULT'


# # Email Templates.

# def emailTemplate(request):
#     return render(request, "app/new-account-mail.html")

# # Paytm Payment gateway Integration

# def paytm(request):
#     amount= str(request.POST['amount'])
#     order_id='order_'+str(datetime.datetime.now().timestamp())
#     custId = request.user.email
#     paytmParams = dict()

#     paytmParams["body"] = {
#         "requestType"   : "Payment",
#         "mid"           : PAYTM_MID,
#         "websiteName"   : PAYTM_WEBSITE,
#         "orderId"       : order_id,
#         "callbackUrl"   : "https://52pattimall.com/app/handlerequest/",
#         "txnAmount"     : {
#             "value"     : amount,
#             "currency"  : "INR",
#         },
#         "userInfo"      : {
#             "custId"    : custId,
#         },
#     }

#     # Generate checksum by parameters we have in body
#     # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
#     checksum = Checksum.generateSignature(json.dumps(paytmParams["body"]), PAYTM_MERCHANT_KEY)

#     paytmParams["head"] = {
#         "signature"    : checksum
#     }

#     post_data = json.dumps(paytmParams)

#     url = PAYTM_ENVIRONMENT+"/theia/api/v1/initiateTransaction?mid="+PAYTM_MID+"&orderId="+order_id

#     response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
#     response_str = json.dumps(response)
#     res = json.loads(response_str)
#     if res["body"]["resultInfo"]["resultStatus"]=='S':
#         token=res["body"]["txnToken"]
#     else:
#         token=""

#     dataParams = {'mid':PAYTM_MID, 'amount':amount, 'orderid':order_id, 'env':PAYTM_ENVIRONMENT, 'token':token}
#     return render(request, 'app/index1.html', dataParams)




# @csrf_exempt
# def handlerequest(request):

#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]


#     verify = Checksum.verifySignature(response_dict, PAYTM_MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             transaction_id = response_dict['BANKTXNID']
#             amount = response_dict['TXNAMOUNT']
#             print('order successful')
#             return redirect('/app/payment-success/'+transaction_id+'/'+amount)
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request, 'app/paymentstatus.html', {'response': response_dict})


#     # data = dict()
#     # data = request.POST
#     # for i in data:
#     #     print(data[i])
#     # if data:
#     #     checksum = data['CHECKSUMHASH']
        
#     #     data.pop('CHECKSUMHASH', None)
        
#     #     #verify checksum
#     #     verifySignature = Checksum.verifySignature(data,PAYTM_MERCHANT_KEY, checksum)
#     #     text_error = ''
#     #     text_success = ''

#     #     if verifySignature:
#     #         text_success = "Checksum is verified.Transaction details are below"
#     #     else:
#     #         text_error = "Checksum is not verified."
#     # else :
#     #     text_error = "Empty POST Response."

#     # dataParams = {'data':data,  'text_success':text_success, 'text_error':text_error, 'verifySignature':verifySignature}
#     # return render(request,'app/callback.html', dataParams)


#     # paytm will send you post request here
#     # MERCHANT_ID =  'wdRVdJ51632956452397'
#     # MERCHANT_KEY = 'jJ819wGiAlcp1eH0'
#     # form = request.POST
#     # response_dict = {}
#     # for i in form.keys():
#     #     response_dict[i] = form[i]
#     #     if i == 'CHECKSUMHASH':
#     #         checksum = form[i]

#     # verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     # if verify:
#     #     if response_dict['RESPCODE'] == '01':

#     #         amount = response_dict['TXNAMOUNT']
#     #         transaction_id = response_dict['TXNID']
#     #         return redirect('/app/payment-success/'+transaction_id+'/'+str(amount))
#     #     else:
#     #         print('order was not successful because' + response_dict['RESPMSG'])
#     # return render(request, 'app/paymentStatus.html', {'response': response_dict})

# # Payment Integration view 
# def Payment_Request(request):
# 	API_KEY = "7a27aefe-9882-43ef-bd63-8f22f3ba654a"
# 	SALT = "accce930013f152866e9ed8fc1af3ab6d1c14b54"
# 	URL = "https://biz.aggrepaypayments.com/v2/paymentrequest"
# 	posted={}
    
# 	for i in request.POST:
# 		posted[i]=request.POST[i]
        
    
# 	hashSequence = "address_line_1|address_line_2|amount|api_key|city|country|currency|description|email|mode|name|order_id|phone|return_url|state|udf1|udf2|udf3|udf4|udf5|zip_code";

# 	hash_string=SALT
# 	hashVarsSeq=hashSequence.split('|')
	
# 	for i in hashVarsSeq:
# 		if i in posted.keys():
# 			if len(str(posted[i])) > 0: 
# 				hash_string+='|'
# 				hash_string+=str(posted[i])
    
# 	hash=hashlib.sha512(hash_string.encode()).hexdigest().upper()
# 	print(hash_string)
    
    
# 	if(	posted.get("amount")!='' and posted.get("amount")!=None and
# 		posted.get("address_line_1")!='' and posted.get("address_line_1")!=None and	
# 		posted.get("city")!='' and posted.get("city")!=None and	
# 		posted.get("name")!='' and posted.get("name")!=None and	
# 		posted.get("email")!='' and posted.get("email")!=None and	
# 		posted.get("mode")!='' and posted.get("mode")!=None and	
# 		posted.get("phone")!='' and posted.get("phone")!=None and	
# 		posted.get("order_id")!='' and posted.get("order_id")!=None and	
# 		posted.get("currency")!='' and posted.get("currency")!=None and	
# 		posted.get("description")!='' and posted.get("description")!=None and	
# 		posted.get("country")!='' and posted.get("country")!=None and	
# 		posted.get("return_url")!='' and posted.get("return_url")!=None ):
		
        
# 		return render(request,'app/payment_request.html',{"posted":posted,"hash":hash,"API_KEY":API_KEY,"action":"https://biz.aggrepaypayments.com/v2/paymentrequest" })
        
# 	else:
# 		hash=''
# 		return render(request,'app/payment_request.html',{"posted":posted,"hash":hash,"API_KEY":API_KEY,"action":"." })
    

# @csrf_protect
# @csrf_exempt
# def Payment_Response(request):
# 	c = {}
# 	c.update(csrf(request))
# 	response_code=request.POST["response_code"]
# 	transaction_id=request.POST["transaction_id"]
# 	response_message=request.POST["response_message"]
# 	amount=request.POST["amount"]
# 	hash=request.POST["hash"]
# 	SALT = "accce930013f152866e9ed8fc1af3ab6d1c14b54"
# 	hash_string=SALT
	
# 	for i in sorted(request.POST):
# 		if(i!='hash'):
# 			if len(request.POST[i]) > 0: 
# 				hash_string+='|'
# 				hash_string+=request.POST[i]
				
# 	calculated_hash=hashlib.sha512(hash_string.encode()).hexdigest().upper()
# 	if(hash == calculated_hash):			
# 		if(response_code == '0'):
# 			return redirect('/app/payment-success/'+transaction_id+'/'+str(amount))
# 		else:	
# 			return render(request,"app/failure.html",{"response_message":"Transaction Failed"})
# 	else:
# 			return render(request,"app/failure.html",{"response_message":"Hash Mis matched , Transaction Failed"})
		

# # User Authentication Views
# @csrf_exempt      
# def userLoginPage(request):
#     if request.user.is_authenticated:
#         return redirect('/app') 
#     return render(request, 'app/login.html')

# def forgotPassword(request):
#     if request.user.is_authenticated:
#         return redirect('/app') 
#     return render(request, 'app/forgot-password.html')

# def resetPasswordLink(request):
#     email = request.POST['email'] 
#     if User.objects.filter(username=email).exists():
#         subject = 'Jodi Win - Password reset link'
#         randomNumber = random.randint(0000, 9999)
#         message = f'Dear Sir/ Madam,\n\nYour 52 Patti Mall -  User account reset password OTP is - '+str(randomNumber)+' \n\nNote - Do not share OTP with any one'
        
#         email_from = settings.EMAIL_HOST_USER
        
#         recipient_list = [email]
        
#         send_mail( subject, message, email_from, recipient_list )
        
#         messages.success(request, "OTP has been sent on your email address")
#         params = {'otp':randomNumber, 'email': email}
#         return render(request, 'app/otp.html', params)

#     else:
#         messages.success(request, 'Entered email address not registered with us, Please enter registered email address')
#         return redirect('forgotPassword')

# def checkOtp(request):
#     otp = request.POST['otp'] 
#     adminOtp = request.POST['adminOtp']
#     email = request.POST['email']

#     if int(otp) == int(adminOtp):
#         params = {'email':email}
#         return render(request, 'app/create-password.html', params)
#     else:
#         messages.success(request, "Entered OTP not match , Enter valid otp")
#         params = {'otp':adminOtp, 'email':email}
#         return render(request, 'app/otp.html', params)
    
# def createNewPassword(request):
#     password = request.POST['password'] 
#     email = request.POST['email']

#     u = User.objects.get(username = email)
#     u.set_password(password)
#     u.save()
#     messages.success(request, "New password has been ctreated, Please login with new password")
#     return redirect('/app/user-login-page')

# def userLoginAppy(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             messages.success(request,'Login Successfull')
#             return redirect('/app')
#             # return HttpResponse("Login Successfull")
#         else:
#             messages.success(request,'Invalid Credentials')
#             return redirect('userLoginPage')
#     return HttpResponse("Make sure method is POST")

# def userLogout(request):
#     logout(request)
#     messages.error(request,'Logout')
#     return redirect('userLoginPage')

# def userRegistrationPage(request):
#     return render(request, 'app/registration.html')

# def userRegistrationApply(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']   
#         username = request.POST['email']
#         phone = request.POST['phone']
#         password1 = request.POST['password']
        
#         if User.objects.filter(username=username).exists():
#             messages.success(request, 'User name already exists with us')
#             return redirect("userRegistrationPage")
#         elif User.objects.filter(email=email).exists():
#             messages.success(request, 'Email already exists')
#             return redirect("userRegistrationPage")
#         else:    
#             newUser= User.objects.create_user(password=password1,email=email,first_name=name,username=username)
#             newUser.save()
#             user = User.objects.get(username = username)

#             roll = UserRoll(user = user, roll = 'customer')
#             roll.save()
#             rollObj = UserRoll.objects.get(user_id = user)
            
#             newCustomer = Customer(phone= phone, status= 'Active', user= user , roll = rollObj, walletAmount= 0)
#             newCustomer.save()

#             # Create Notification 
#             customer = Customer.objects.get(user = user)
#             notification = Notifications(customer= customer, title= "New Account Created Successfully", msg= "New user account created recently", date = datetime.datetime.now(), status = 'Account Active')
#             notification.save()

#             # create bank account 
#             bank = BankAccount(customer= customer)
#             bank.save()
#             user = authenticate(request, username=username, password =password1)
#             if user is not None:
#                 login(request,user)
#                 messages.warning(request, 'Your user account has been created.')
#                 return redirect('/app')
#             return redirect('userLoginPage')   


# def aboutUs(request):
#     return render(request, 'app/about-us.html')

# def terms(request):
#     return render(request, 'app/terms.html')

# def privacy(request):
#     return render(request, 'app/privacy.html')

# def refund(request):
#     return render(request, 'app/refund.html')

# def contact(request):
#     return render(request, 'app/contact-us.html')


def home(request):
    pass


# def jodiWin(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.filter(user = request.user.id)
#             jodiMarket = JodiMarket.objects.all()
#             walletBalance = 0
#             for i in customer:
#                 walletBalance = i.walletAmount

#             resultCardsDict ={}
#             resultCards= {}
#             for i in jodiMarket:
#                 if i.result == '**':
#                     pass
#                 else:
#                     resultCards = json.loads(i.result) 
#                     resultCardsDict[i] = {'resultCards': resultCards}
            
            
#             params = {'walletBalance': walletBalance, 'jodiMarket': jodiMarket, 'resultCardsDict':resultCardsDict}
#             return render(request, 'app/jodi-win.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def jodiGameList(request, marketId):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customer:
#                 walletBalance = i.walletAmount

#             game = Games.objects.filter(marketType = 'Jodi-Market')
            
#             params = {'walletBalance': walletBalance, 'game': game, 'marketId': marketId}
#             return render(request, 'app/jodi-game.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def playJodiGame(request, marketId, gameId):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user = request.user.id)
#             bids = JodiBiddingHistory.objects.filter(customer = customer, date = datetime.datetime.now())
#             game = Games.objects.filter(id = gameId)
#             card = Card.objects.all()
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount


#             for i in game:
#                 gameMarket= i.marketType
#                 title = i.title
#             params = {'gameMarket': gameMarket, 'title':title, 'marketId': marketId, 'gameId':gameId, 'bids': bids, 'walletBalance':walletBalance , 'card':card}
#             return render(request, 'app/jodi-bidding.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def placeJodiBid(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             date = request.POST['date']
#             marketId = request.POST['marketId']
#             gameId = request.POST['gameId']
#             resultCard = request.POST['resultCard']
#             points = request.POST['points']
#             marketType = request.POST['marketType']
#             time = timezone.now()
            
#             market = JodiMarket.objects.get(id = marketId)
#             game = Games.objects.get(id = gameId)
#             customerObj = Customer.objects.get(user = request.user.id)

#             if market.status == 'game is closed for today':
#                 messages.warning(request, "Game has been closed, you can't play in this game")
#                 return redirect('/app/jodi-win')
            
            
#             cardPattern= ""
#             # create card pattern 
#             cardDict = json.loads(resultCard)
#             for c in cardDict.values():
#                 cardPattern = cardPattern + str(c[0])
#             print(cardPattern)

#             availabeBalance = 0
#             customer = Customer.objects.filter(user = request.user.id)
#             for i in customer:
#                 availabeBalance = i.walletAmount
            
#             if int(points) <= int(availabeBalance):
#                 newBid = JodiBiddingHistory(customer = customerObj, market= market, game=game, points=points, resultCard= resultCard, cardPattern= cardPattern,
#                 date =datetime.datetime.now(), time= time, status = 'Bidding Placed' )
#                 newBid.save()

#                 customerObj.walletAmount = availabeBalance - int(points)
#                 customerObj.save()

#                 brokerWallet = 0
#                 if PartnerUser.objects.filter(user_id = customerObj.id).exists():
#                     brokerUser = PartnerUser.objects.get(user_id = customerObj.id)
#                     broker = Partner.objects.get(id = brokerUser.partner.id)
#                     broker.payingBiddingAmount = broker.payingBiddingAmount + int(points)
#                     broker.save()
                    
#                 messages.success(request, "game placed Successfull")
                
#                 return redirect('/app/play-jodi-game/'+str(marketId)+'/'+str(gameId))
#             else:
#                 messages.success(request, "Insufficient funds, Please recharge wallet first")
                
#                 return redirect('/app/add-funds')
#             customer = Customer.objects.get(user = request.user.id)

#             params = {'gametype': 'jodi', 'marketId': marketId, 'gameId':gameId }
#             return render(request, 'app/bidding.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def addFund(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.filter(user = request.user.id)
#             trCount = Transaction.objects.all().count()
#             randomNumber = random.randint(0000000, 9999999)

#             orderId = str(trCount) + str(randomNumber)
#             walletBalance = 0
#             for i in customer:
#                 walletBalance = i.walletAmount
#                 phone = i.phone    
#             params = {'walletBalance': walletBalance, 'orderId':orderId, 'phone':phone}
#             return render(request, 'app/addmoney.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def makePayment(request, amount):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
            
#             # Razor Pay Secrate Key 
#             RAZORPAY_API_KEY = 'rzp_test_6N07iyfMNAAsWu'
#             RAZORPAY_SECRATE_KEY = 'afPDAQrxtbSCnJVpiz3VophS'

#             if amount == 0:
#                 client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_SECRATE_KEY))
                
#                 order_amount = int(request.POST['amount'])*100
#                 order_currency = 'INR'
#                 notes = {'Shipping address': "Adding Fund in user wallet"}
#                 name= request.user.first_name
#                 email = request.user.email  

#                 customer = Customer.objects.filter(user_id= request.user.id)
#                 for i in customer:
#                     phone = i.phone
#                 payment_order = client.order.create(dict( amount=order_amount, currency=order_currency, notes=notes, payment_capture=1))
#                 payment_order_id = payment_order['id']

#                 context ={'amount': order_amount, 'api_key': RAZORPAY_API_KEY, 'order_id': payment_order_id, 'customerName': name, 
#                 'customerEmail': email, 'customerContact' :phone, 'orderDate': datetime.datetime.now()}    

#                 return render(request, "app/order-success.html", context)
#             else:
#                 return HttpResponse('Hello '+amount)                
#             return render(request, 'app/addmoney.html')
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def paymentSuccess(request,successPaymentId,amount):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             walletAmt = 0
#             wallet = Customer.objects.filter(user_id = request.user.id)
#             for i in wallet:
#                 walletAmt = i.walletAmount

#             customer = Customer.objects.get(user_id = request.user.id)
#             customer.walletAmount = walletAmt + float(amount)
#             customer.save()

#             trasanction = Transaction(customer = customer, amount= float(amount), transactionType = "Online", transactionMode= "Bank Transfer",  successPaymentId = successPaymentId,  date = datetime.datetime.now())

#             trasanction.save()
#             messages.success(request, "Fund addedd successfully in wallet")
#             return redirect('/app')
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')


# def gameList(request, id):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customer:
#                 walletBalance = i.walletAmount

#             game = Games.objects.filter(marketType = 'Reguler Market')
#             params ={ 'marketId': id, 'game': game, walletBalance: walletBalance}                    
#             return render(request, 'app/game.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def playGame(request, marketId, gameId):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user = request.user.id)
#             card = Card.objects.all()
#             bids = BiddingHistory.objects.filter(customer = customer, date = datetime.datetime.now())
#             game = Games.objects.filter(id = gameId)
#             market = Market.objects.get(id = marketId)
#             status = market.status
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount


#             for i in game:
#                 gameMarket= i.marketType
#                 title = i.title
#             params = {'gameMarket': gameMarket, 'title':title, 'marketId': marketId, 'gameId':gameId, 'bids': bids, 'walletBalance':walletBalance , 'status':status, 'card': card}
#             if gameId == 10:
#                 return render(request, 'app/single-ank-bidding.html', params)
#             elif gameId == 6:
#                 return render(request, 'app/double-panna.html', params)
#             elif gameId == 1:
#                 return render(request, 'app/single-panna.html', params)
#             elif gameId == 3:
#                 return render(request, 'app/triple-panna.html', params)
#             elif gameId == 4:
#                 return render(request, 'app/bidding.html', params)
#             return HttpResponse("Game not availabel")
            
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def placeBid(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             date = request.POST['date']
#             marketId = request.POST['marketId']
#             gameId = request.POST['gameId']
#             rummyCard = request.POST['rummyCard']
#             jokerCard = request.POST['jokerCard']

#             cardPattern= ""
#             # create card pattern 
#             rummyCardDict = json.loads(rummyCard)
#             for c in rummyCardDict.values():
#                 cardPattern = cardPattern + str(c[0])
#             jokerCardDict = json.loads(jokerCard)
#             for c in jokerCardDict.values():
#                 cardPattern = cardPattern + str(c[0])

#             print(cardPattern)
#             market = Market.objects.get(id = marketId)
#             game = Games.objects.get(id = gameId)
#             customerObj = Customer.objects.get(user = request.user.id)
#             points = request.POST['points']
#             marketType = request.POST['marketType']

#             if market.status == 'game is closed for today':
#                 messages.warning(request, "Market has been closed, you can't play game in this market")
#                 return redirect('/app')
#             elif market.status == "game is running for close":
#                 if marketType == "open":
#                     messages.warning(request, "Market has been closed for open, Please play for close ")
#                     return redirect('/app')

                
#             time = timezone.now()

#             availabeBalance = 0
#             customer = Customer.objects.filter(user = request.user.id)
#             for i in customer:
#                 availabeBalance = i.walletAmount
                

#             if int(points) <= int(availabeBalance):
#                 newBid = BiddingHistory(customer = customerObj, market= market, game=game, rummyCard = rummyCard , jokerCard= jokerCard, points=points, cardPattern = cardPattern,
#                 date =datetime.datetime.now(), time= time, status = 'Bidding Placed', marketType=marketType )
#                 newBid.save()

#                 customerObj.walletAmount = availabeBalance - int(points)
#                 customerObj.save()

#                     # Broker Walet Update 
#                 brokerWallet = 0
#                 if PartnerUser.objects.filter(user_id = customerObj.id).exists():
#                     brokerUser = PartnerUser.objects.get(user_id = customerObj.id)
#                     broker = Partner.objects.get(id = brokerUser.partner.id)
#                     broker.payingBiddingAmount = broker.payingBiddingAmount + int(points)
#                     broker.save()
                        
#                 messages.success(request, "Game placed Successfull")
                    
#                 return redirect('/app/play-game/'+str(marketId)+'/'+str(gameId))
#             else:
#                 messages.success(request, "Insufficient funds, Please recharge wallet first")
#                 return redirect('/app/add-funds')
                
#             customer = Customer.objects.get(user = request.user.id)

#             params = {'gametype': 'jodi', 'marketId': marketId, 'gameId':gameId }
#             return render(request, 'app/bidding.html', params)
            
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def placeBidMegalot(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             date = request.POST['date']
#             marketId = request.POST['marketId']
#             gameId = request.POST['gameId']
#             rummyCard = request.POST['rummyCard']
#             jokerCard = request.POST['jokerCard']

#             openCardPattern= ""
#             closeCardPattern= ""

#             # create card pattern 
#             rummyCardDict = json.loads(rummyCard)
#             jokerCardDict = json.loads(jokerCard)
#             rummyCount = 0
#             jokerCount = 0


#             # OPenCard Result 
#             for c in rummyCardDict.values():
#                 if(rummyCount < 3):
#                     openCardPattern = openCardPattern + str(c[0])
#                     rummyCount = rummyCount + 1
#                 else:
#                     closeCardPattern = closeCardPattern + str(c[0])
            
            

#             for c in jokerCardDict.values():
#                 if(jokerCount < 1):
#                     openCardPattern = openCardPattern + str(c[0])
#                     jokerCount = jokerCount + 1
#                 else:
#                     closeCardPattern = closeCardPattern + str(c[0])
                    
#             print(closeCardPattern)
#             print(closeCardPattern)  
            

#             cardPattern = openCardPattern + closeCardPattern
             

#             print(cardPattern)
#             market = Market.objects.get(id = marketId)
#             game = Games.objects.get(id = gameId)
#             customerObj = Customer.objects.get(user = request.user.id)
#             points = request.POST['points']
#             marketType = request.POST['marketType']

#             if market.status == 'game is closed for today':
#                 messages.warning(request, "Market has been closed, you can't play game in this market")
#                 return redirect('/app')
#             elif market.status == "game is running for close":
#                 if marketType == "open":
#                     messages.warning(request, "Market has been closed for open, Please play for close ")
#                     return redirect('/app')

                
#             time = timezone.now()

#             availabeBalance = 0
#             customer = Customer.objects.filter(user = request.user.id)
#             for i in customer:
#                 availabeBalance = i.walletAmount
                

#             if int(points) <= int(availabeBalance):
#                 newBid = BiddingHistory(customer = customerObj, market= market, game=game, rummyCard = rummyCard , jokerCard= jokerCard, points=points, cardPattern = cardPattern,
#                 date =datetime.datetime.now(), time= time, status = 'Bidding Placed', marketType=marketType )
#                 newBid.save()

#                 customerObj.walletAmount = availabeBalance - int(points)
#                 customerObj.save()

#                     # Broker Walet Update 
#                 brokerWallet = 0
#                 if PartnerUser.objects.filter(user_id = customerObj.id).exists():
#                     brokerUser = PartnerUser.objects.get(user_id = customerObj.id)
#                     broker = Partner.objects.get(id = brokerUser.partner.id)
#                     broker.payingBiddingAmount = broker.payingBiddingAmount + int(points)
#                     broker.save()
                        
#                 messages.success(request, "Game placed Successfull")
                    
#                 return redirect('/app/play-game/'+str(marketId)+'/'+str(gameId))
#             else:
#                 messages.success(request, "Insufficient funds, Please recharge wallet first")
#                 return redirect('/app/add-funds')
                
#             customer = Customer.objects.get(user = request.user.id)

#             params = {'gametype': 'jodi', 'marketId': marketId, 'gameId':gameId }
#             return render(request, 'app/bidding.html', params)
            
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# # Rules & Notice Board
# def noticeBoard(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount
            
#             params={'walletBalance': walletBalance}
#             return render(request, 'app/rules.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')


# # History
# def history(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount
            
#             params={'walletBalance': walletBalance}
#             return render(request, 'app/history.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def biddingHistory(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user = request.user.id)
#             bids = BiddingHistory.objects.filter(customer = customer, date = datetime.datetime.now())
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount

#             rummyCardDict ={}
#             jokerCardDict ={}

#             for i in bids:
#                 if i.rummyCard == '***':
#                     pass
#                 else:
#                     rummyCards = json.loads(i.rummyCard) 
#                     rummyCardDict[i] = {'rummyCards': rummyCards}
                    
#                 if i.jokerCard == '*':
#                     pass
#                 else:
#                     jokerCards = json.loads(i.jokerCard) 
#                     jokerCardDict[i] = {'jokerCards':jokerCards}


#             params={'bids': bids, 'walletBalance': walletBalance, 'rummyCardDict':rummyCardDict, 'jokerCardDict':jokerCardDict}
#             return render(request, 'app/bidding-history.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def jodiWinBidHistory(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user = request.user.id)
#             bids = JodiBiddingHistory.objects.filter(customer = customer, date = datetime.datetime.now())
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount

#             resulrCardDict ={}
#             for i in bids:
#                 if i.resultCard == '':
#                     pass
#                 else:
#                     resultCards = json.loads(i.resultCard) 
#                     resulrCardDict[i] = {'resultCards': resultCards}

#             params={'bids': bids, 'walletBalance': walletBalance, 'resulrCardDict':resulrCardDict}
#             return render(request, 'app/jodi-win-bid-history.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')


# def bidResultHistory(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user = request.user.id)
#             bids = BiddingHistory.objects.filter(customer = customer, status= 'win')
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount

#             rummyCardDict ={}
#             jokerCardDict ={}

#             for i in bids:
#                 if i.rummyCard == '***':
#                     pass
#                 else:
#                     rummyCards = json.loads(i.rummyCard) 
#                     rummyCardDict[i] = {'rummyCards': rummyCards}
                    
#                 if i.jokerCard == '*':
#                     pass
#                 else:
#                     jokerCards = json.loads(i.jokerCard) 
#                     jokerCardDict[i] = {'jokerCards':jokerCards}

#             params={'bids': bids, 'walletBalance': walletBalance, 'rummyCardDict':rummyCardDict, 'jokerCardDict':jokerCardDict}
#             return render(request, 'app/bid-result-history.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def jodiWinResultHistory(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user = request.user.id)
#             bids = JodiBiddingHistory.objects.filter(customer = customer, status= 'win')
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount

#             resulrCardDict ={}
#             for i in bids:
#                 if i.resultCard == '':
#                     pass
#                 else:
#                     resultCards = json.loads(i.resultCard) 
#                     resulrCardDict[i] = {'resultCards': resultCards}

#             params={'bids': bids, 'walletBalance': walletBalance, 'resulrCardDict':resulrCardDict}
#             return render(request, 'app/jodi-win-result-history.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')


# # Bid Details 
# def bidDetails(request, id):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user = request.user.id)
#             bids = BiddingHistory.objects.filter(id = id)
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount

#             params={'bids': bids, 'walletBalance': walletBalance}
#             return render(request, 'app/bid-details.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def jodiWinBidDetails(request, id):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user = request.user.id)
#             bids = JodiBiddingHistory.objects.filter(id = id)
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount

#             params={'bids': bids, 'walletBalance': walletBalance}
#             return render(request, 'app/jodi-win-bid-details.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def withdraw(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customer:
#                 walletBalance = i.walletAmount

#             params ={'walletBalance': walletBalance}    
#             return render(request, 'app/withdraw.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def pendingWithdrawRequest(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user_id = request.user.id)
#             pending = Withdraw.objects.filter(customer = customer, status= 'New')

#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount

#             params = {'pending': pending, 'date': datetime.datetime.now(), 'walletBalance': walletBalance}

#             return render(request, 'app/pending-withdraw.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def sendWithdrawRequest(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
            
#             customer = Customer.objects.get(user = request.user.id)

#             amount = request.POST['amount']
#             remark = request.POST['remark']

#             availabeBalance = 0
#             customer = Customer.objects.get(user = request.user.id)
#             availabeBalance = customer.walletAmount  
#             if availabeBalance < 2000:
#                 messages.success(request, "Wallet balance must be more than Rs.2000")        
#                 return redirect('/app/withdraw')

#             balance = availabeBalance - int(amount) 
#             if balance < 2000:    
#                 messages.success(request, "You must be maintain Rs.2000 minimum balance.")        
#                 return redirect('/app/withdraw')

#             if int(amount) <= int(availabeBalance):
#                 withdraw = Withdraw(customer = customer, amount= amount, date = datetime.datetime.now())
#                 withdraw.save()
#                 customer.walletAmount = customer.walletAmount - int(amount)
#                 customer.save()
#                 messages.success(request, "Withdraw request sent.")
#                 return redirect('pendingWithdrawRequest')

#             messages.success(request, "Insufficient funds.")        
#             return redirect('/app/withdraw')
            
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def accountStatement(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user_id = request.user.id)
#             transaction = Transaction.objects.filter(customer = customer)
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount

#             params = {'transaction': transaction, 'date': datetime.datetime.now(), 'walletBalance':walletBalance}

#             return render(request, 'app/transaction.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')


# # Top Winners 
# def topWinners(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user = request.user.id)
#             topWinners = BiddingHistory.objects.filter(status = 'win', date= datetime.datetime.now())
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount

#             params={'topWinners': topWinners, 'walletBalance': walletBalance}
#             return render(request, 'app/top-winners.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def topJodiWinners(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.get(user = request.user.id)
#             topWinners = JodiBiddingHistory.objects.filter(status = 'win', date= datetime.datetime.now())
            
#             customerObj = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customerObj:
#                 walletBalance = i.walletAmount

#             params={'topWinners': topWinners, 'walletBalance': walletBalance}
#             return render(request, 'app/top-jodi-winners.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# # Games Rate 
# def gameRate(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             rates = Games.objects.all()
#             customer = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customer:
#                 walletBalance = i.walletAmount
            
#             params = {'rates': rates, 'date': datetime.datetime.now(), 'walletBalance':walletBalance }
#             return render(request, 'app/game-rate.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')


# def notifications(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customer:
#                 walletBalance = i.walletAmount
#                 id =i.id

#             notification =Notifications.objects.filter(customer_id = id)    
#             params = {'walletBalance':walletBalance, 'notification':notification }
#             return render(request, 'app/notification.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')


# def profile(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.filter(user = request.user.id)
#             walletBalance = 0
#             for i in customer:
#                 walletBalance = i.walletAmount
#                 id =i.id
#             bank = BankAccount.objects.filter(customer_id = id)
#             notification =Notifications.objects.filter(customer_id = id)    
#             params = {'walletBalance':walletBalance, 'customer':customer, 'bank':bank }
#             return render(request, 'app/profile.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')


# def updateBankDetails(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             customer = Customer.objects.filter(user = request.user.id)
#             customerObj = Customer.objects.get(user = request.user.id)
#             walletBalance = 0
#             for i in customer:
#                 walletBalance = i.walletAmount
#                 id =i.id
#             bank = BankAccount.objects.get(customer_id = id)
            
#             bank.bankName= request.POST['bankName']
#             bank.accountName= request.POST['accountName']
#             bank.accountNumber= request.POST['accountNumber']
#             bank.ifscCode= request.POST['ifscCode']
#             bank.date = datetime.datetime.now()
#             bank.status = 'Bank Details Updated'
#             bank.save()    

#             notification = Notifications(customer =customerObj, title="Bank details update", msg = 'bank details updated by user', date =datetime.datetime.now(), status= 'Account Active' )
#             notification.save()

#             messages.success(request, "Bank detials updated")
#             return redirect('/app/profile')
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')


# def brokerRegister(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             return render(request, 'app/broker-register-page.html')
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')



# def brokerRegistrationApply(request):
#     if request.method == 'POST':
#         address = request.POST['address']
#         city = request.POST['city']   
#         panNumber = request.POST['panNumber']
        
#         user = User.objects.get(id = request.user.id) 
#         customer = Customer.objects.get(user_id = request.user.id)
#         bankAccount = BankAccount.objects.get(customer_id = customer.id)

#         if Partner.objects.filter(user_id= request.user.id).exists():
#             messages.success(request, 'Your broker account already created with us, Please try with another user account')
#             return redirect("/app")
#         else:
#             partner = Partner(user = user, phone = customer.phone, city = city, address= address, panNumber= panNumber, bankName=bankAccount.bankName, accountNumber= bankAccount.accountNumber,  ifscCode = bankAccount.ifscCode)

#             partner.save()
#             subject = '52 Patti Mall - Broker account created successfully'
#             message = f'Dear Sir/ Madam ,\nCongratulations,\n\nYour 52 Patti Mall - Broker account has been created successfully. \nclick on link to login broker admin panel - http://52pattimall.com/partner \n\nNote - Username & password will be same of 52 Patti Mall user account'
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [user.email]
#             send_mail( subject, message, email_from, recipient_list )

#             messages.success(request, "Your broker account has been created, Please check email for login to broker panel")
#             return redirect('/app')
    

# def jodiGamePanelChart(request,id):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             chart = PanelChartJodiMarket.objects.filter(market_id= id)
#             params = {'chart':chart}
#             return render(request, 'app/panel-chart.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def regulerGamePanelChart(request,id):
#     if request.user.is_authenticated:
#         if request.user.is_superuser == 0:
#             chart = PanelChartRegulerMarket.objects.filter(market_id= id)
#             params = {'chart':chart}
#             return render(request, 'app/reguler-market-panel-chart.html', params)
#         messages.success(request, 'You are not authorized to access') 
#         return render(request, 'app/login.html')
#     return redirect('userLoginPage')

# def addCart(request):
#     return render(request, 'app/add-card.html')

# def addNewCart(request):
#     name = request.POST['name']
#     value= request.POST['value']
#     category= request.POST['category']
#     image = request.FILES['image']

#     newCard  = Card(name = name, value=value, image= image, category= category)
#     newCard.save()

#     return redirect('addCart')