
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login,logout
from dashboard.models import Dealer, Distributor, Transaction, Product, Order, Inbox , AdminNotifications, UserNotifications
from django.contrib import messages
from django.db.models import Count, F, Value, Q
from django.db.models.functions import Length, Upper
import datetime
import http.client
import razorpay
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout 
from django.db.models import Sum
import json
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from pattiMallProj.decorators import check_admin_account

# User Authentication Views

def adminLogin(request):
    if request.user.is_authenticated:
        return redirect('/dashboard') 
    return render(request, 'dashboard/login.html')

def handleAdminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'Login Sucessfull')
            return redirect('/dashboard')
            # return HttpResponse("Login Successfull")
        else:
            messages.success(request,'Invalid Credentials')
            return redirect('adminLogin')
    return render(request, "dashboard/error.html")

def adminLogout(request):
    logout(request)
    messages.success(request,'Logout')
    return redirect('/dashboard/admin-login')



@login_required(login_url = '/dashboard/admin-login')
@check_admin_account()
def home(request):
    productsCount = Product.objects.all().count()
    ordersCount = Order.objects.all().count()
    memebrsCount = Dealer.objects.all().count()
    adminNotications = AdminNotifications.objects.filter(status = 'new').order_by('-id')
    adminNoticationsCount = AdminNotifications.objects.filter(status = 'new').count()
    
    approvedMemebrsCount = Dealer.objects.filter(status = 'approved').count()
    pendingMemebrsCount = Dealer.objects.filter(status = 'under-review').count()

    underReviewMemebrs = Distributor.objects.filter(status = 'under-review').order_by('-id')
    transactions = Transaction.objects.filter(status = 'approved').order_by('-id')
    paidBalance = Dealer.objects.all().aggregate(Sum('paidBalance'))
    pendingBalance = Dealer.objects.all().aggregate(Sum('walletBalance'))
    sales  = Order.objects.all().aggregate(Sum('amount'))
    msgs = Inbox.objects.filter(status = 'new').count()

    # Calculate Revenue
    revenue = 0 
    dealer  = Dealer.objects.filter(status = 'approved')
    for i in dealer:
        revenue = revenue + int(i.product.price)
    
    # netBalance = (float(revenue)) - (float(paidBalance['paidBalance__sum']) + float(pendingBalance['walletBalance__sum']))
    netBalance = 0

    # Graph Inputs 
    today = datetime.datetime.now()
    yestarday = today - datetime.timedelta(days = 1)


    currentMonth = datetime.datetime.now().month
    dealerDate = Dealer.objects.filter(date__month=currentMonth)
    
    graphdata = {}
    for x in range(5, currentMonth + 1):
        dCount = Dealer.objects.filter(date__month= x ).count()
        # print('Month is :'+str(x)+' and dealers are :'+ str(dCount))
        graphdata[x] = dCount
     
    print('Total Dealers in graph data is : '+ str(graphdata))


    params = {'productsCount':productsCount, 'ordersCount':ordersCount, 'memebrsCount':memebrsCount, 'revenue':revenue, 'paidBalance':paidBalance, 'pendingBalance':pendingBalance , 'netBalance':netBalance, 'sales':sales, 'msgs':msgs, 'approvedMemebrsCount':approvedMemebrsCount, 'pendingMemebrsCount':pendingMemebrsCount, 'underReviewMemebrs':underReviewMemebrs, 'transactions':transactions, 'graphdata':graphdata, 'adminNotications':adminNotications, 'adminNoticationsCount':adminNoticationsCount}
    return render(request, 'dashboard/index.html', params)
      
# Members Management
@login_required(login_url = '/dashboard/admin-login')
@check_admin_account()
def members(request, status):
    if status == 'approved':
        members = Dealer.objects.filter(status = 'approved').order_by('-id')
    else:
        members = Distributor.objects.filter(status = status)


    params = {'members':members, 'status':status} 
    return render(request, 'dashboard/members.html',params)

@login_required(login_url = '/dashboard/admin-login')
@check_admin_account()
def memberDetails(request, id):
    totalMember = 0 
    totalRevenue = 0
    member = Dealer.objects.get(id = id )
    directMembers = Distributor.objects.filter(dealer_id = id, status = 'approved')
    directMembersCount = Distributor.objects.filter(dealer_id = id, status = 'approved').count()
    totalMember = totalMember + directMembersCount

    wb = 0 
    level1 = {}
    level2 = {}
    level3 = {}
    level4 = {}
    level5 = {}

    # Varibale Declarations 
    level1Total, level12Total, level3Total, level4Total, level5Total = 0 , 0, 0, 0, 0
    level1Earing, level2Earing, leve3Earing, leve4Earing, leve5Earing = 0 , 0, 0, 0, 0
    # First Level For Loop 
    for i in directMembers:
        directMembersCount = directMembersCount
        
        level1Total = level1Total + int(i.product.price) 
        level1Earing = float(level1Total) * float(10) / 100
        totalRevenue = totalRevenue + level1Earing
        level1 = {'directMembersCount':directMembersCount, 'level1Total':level1Total, 'level1Earing':level1Earing}
        

        if Dealer.objects.filter(phone = i.phone).exists():
            level2Dealer = Dealer.objects.get(phone = i.phone)
            print('Secong level is : '+level2Dealer.user.first_name)
            level2DealerDirectMembers = Distributor.objects.filter(dealer_id = level2Dealer.id)
            print('\nDistributor of '+level2Dealer.user.first_name+' is '+str(level2DealerDirectMembers))
            level2DealerDirectMembersCount = Distributor.objects.filter(dealer_id = level2Dealer.id).count()
            totalMember = totalMember + level2DealerDirectMembersCount
            # Second Level For Loop
            for si in level2DealerDirectMembers:
                level12Total = level12Total + int(si.product.price)
                level2Earing = float(level12Total) * float(5) / 100
                
                level2 ={'level2DealerDirectMembersCount': level2DealerDirectMembersCount, 'level12Total':level12Total, 'level2Earing':level2Earing}
                
                if Dealer.objects.filter(phone = si.phone).exists():
                    level3Dealer = Dealer.objects.get(phone = si.phone)
                    print('Third level is : '+level3Dealer.user.first_name)
                    level3DealerDirectMembers = Distributor.objects.filter(dealer_id = level3Dealer.id)
                    print('\nDistributor of '+level3Dealer.user.first_name+' is '+str(level3DealerDirectMembers))
                    level3DealerDirectMembersCount = Distributor.objects.filter(dealer_id = level3Dealer.id).count()
                    totalMember = totalMember + level3DealerDirectMembersCount
                    # Third Level For Loop
                    for ti in level3DealerDirectMembers:
                        level3Total = level3Total + int(ti.product.price)
                        level3Earing = float(level3Total) * float(2) / 100
                        
                        level3 ={'level3DealerDirectMembersCount': level3DealerDirectMembersCount, 'level3Total':level3Total, 'level3Earing':level3Earing}

                        if Dealer.objects.filter(phone = ti.phone).exists():
                            level4Dealer = Dealer.objects.get(phone = ti.phone)
                            print('Fourth level is : '+level4Dealer.user.first_name)
                            level4DealerDirectMembers = Distributor.objects.filter(dealer_id = level4Dealer.id)
                            print('\nDistributor of '+level4Dealer.user.first_name+' is '+str(level4DealerDirectMembers))
                            level4DealerDirectMembersCount = Distributor.objects.filter(dealer_id = level4Dealer.id).count()
                            totalMember = totalMember + level4DealerDirectMembersCount
                            # Fourth Level For Loop
                            for fi in level4DealerDirectMembers:
                                level4Total = level4Total + int(fi.product.price)
                                level4Earing = float(level4Total) * float(1) / 100
                                
                                level4 ={'level4DealerDirectMembersCount': level4DealerDirectMembersCount, 'level4Total':level4Total, 'level4Earing':level4Earing}
                                

                                if Dealer.objects.filter(phone = fi.phone).exists():
                                    level5Dealer = Dealer.objects.get(phone = fi.phone)
                                    print('Fifth level is : '+level5Dealer.user.first_name)
                                    level5DealerDirectMembers = Distributor.objects.filter(dealer_id = level5Dealer.id)
                                    print('\nDistributor of '+level5Dealer.user.first_name+' is '+str(level5DealerDirectMembers))
                                    level5DealerDirectMembersCount = Distributor.objects.filter(dealer_id = level5Dealer.id).count()
                                    totalMember = totalMember + level5DealerDirectMembersCount
                                    # Fifth Level For Loop
                                    for fti in level5DealerDirectMembers:
                                        level5Total = level5Total + int(fti.product.price)
                                        level5Earing = float(level5Total) * float(0.5) / 100
                                        
                                        level5 ={'level5DealerDirectMembersCount': level5DealerDirectMembersCount, 'level5Total':level5Total, 'level5Earing':level5Earing}
                                        
                                else:
                                    print('This dealer is not availabel in Fifth level :'+i.name)


                        else:
                            print('This dealer is not availabel in Fouth level :'+i.name)

                print('This dealer is not availabel in Third level :'+i.name)


                
        else:
            print('This dealer is not availabel in second level :'+i.name)


    # Calculate Wallet Balance & Paid Balance 
    if level1:
        wb = level1['level1Earing']
        if level2:
            wb = level1['level1Earing'] + level2['level2Earing']
            if level3:
                wb = level1['level1Earing'] + level2['level2Earing'] + level3['level3Earing']
                if level4:
                    wb = level1['level1Earing'] + level2['level2Earing'] + level3['level3Earing'] + level4['level4Earing']
                    if level5:
                        wb = level1['level1Earing'] + level2['level2Earing'] + level3['level3Earing'] + level4['level4Earing'] + level5['level5Earing']

    totalRevenue = wb
    walletBalance = float(wb) - float(member.paidBalance) 
    member.walletBalance = walletBalance
    member.save()

    params = {'member':member, 'directMembers':directMembers, 'directMembersCount':directMembersCount, 'level1':level1, 'level2':level2, 'level3':level3, 'level4':level4, 'level5':level5, 'totalMember':totalMember, 'totalRevenue':totalRevenue, 'walletBalance':walletBalance}
    return render(request, 'dashboard/member-details.html', params)


def memberDetailsByPhone(request, phone):
    member = Dealer.objects.get(phone = phone )
    return redirect('/dashboard/member-details/'+str(member.id))
    

def deleteMember(request, id):
    member = Dealer.objects.get(id = id )
    member.delete()

    messages.success(request, 'Member Deleted')
    return redirect('/dashboard/members/under-review')

def approveMember(request,id):
    # Update Distributor account
    distributor = Distributor.objects.get(id = id)
    distributor.status = 'approved'
    
    phone = distributor.phone
    sponsored = distributor.sponseredId
    email = distributor.email
    
    distributor.save()

    # Update dealer account 
    dealer = Dealer.objects.get(phone = phone)
    dealer.status = 'approved'
    dealer.save()

    # Update Reference Delaer Pins count 
    refDealer = Dealer.objects.get(phone = sponsored)
    refDealer.pins = refDealer.pins - 1
    refDealer.save()

    # Send Mail to member
    subject = 'Member account approved - Arogyam Ayush'
    message = f'Dear Sir,\nCongratilations,  \n\nYour member account has been approved, Now you can enhance your welth with Arogyam Ayush.\nYou can login to member panel,\n\nThanking you\nTeam Arogyam Ayush'
        
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,'phenoware@gmail.com']
    send_mail( subject, message, email_from, recipient_list )


    messages.success(request, 'Member account has been approved')
    return redirect('/dashboard/members/under-review')


# Financial Management
@login_required(login_url = '/dashboard/admin-login')
@check_admin_account()
def withdrawRequest(request):
    req  = Transaction.objects.filter(status = 'unpaid').order_by('-id')
    params = {'req':req}

    return render(request, 'dashboard/withdraw-request.html', params) 

def deleteRequest(request, id):
    req = Transaction.objects.get(id = id )
    req.status ='rejected'
    req.save()

    # Create Member Notification
    link = '/partner/withdraw-request' 
    memberNotification = UserNotifications(dealer = dealer, status = 'new', msg = 'Your withdraw request rejected', date = datetime.datetime.now(), link = link)
    memberNotification.save()

    messages.success(request, 'Withdraw Request Rejected')
    return redirect('/dashboard/withdraw-request')

def approveRequest(request, id):
    req = Transaction.objects.get(id = id )
    
    dealer = Dealer.objects.get(id = req.dealer.id)
    dealer.paidBalance = dealer.paidBalance + int(req.requestAmount)
    dealer.walletBalance = dealer.walletBalance - int(req.requestAmount)
    dealer.save()

    req.status = 'approved'
    req.paidAmount = req.requestAmount
    req.transactionMode = 'Online'
    req.paidDate = datetime.datetime.now()

    req.save()

    # Create Member Member Notification 
    link = '/partner/transactions' 
    memberNotification = UserNotifications(dealer = dealer, status = 'new', msg = 'Your withdraw request approved', date = datetime.datetime.now(), link = link)
    memberNotification.save()


    messages.success(request, 'Withdraw Request Approved')
    return redirect('/dashboard/withdraw-request')

@login_required(login_url = '/dashboard/admin-login')
@check_admin_account()
def transactions(request):
    transactions = Transaction.objects.filter(status = 'approved').order_by('-id')
    params = {'transactions':transactions}

    return render(request, 'dashboard/transactions.html', params)

def viewNotification(request, id):
    notifiation = AdminNotifications.objects.get(id = id )
    notifiation.status = 'seen'
    notifiation.save()
    return redirect(notifiation.link)

def markAsRead(request):
    notifications = AdminNotifications.objects.filter(status = 'new')
    for i in notifications:
        i.status = 'seen'
        i.save()
    
    messages.success(request, ' Notifications status changed - Mark as read.')
    return redirect('/dashboard')

def msg(request):
    return render(request, 'dashboard/message.html')


# Orders Management
@login_required(login_url = '/dashboard/admin-login')
@check_admin_account()
def orders(request):
    orders = Order.objects.all().order_by('-id')

    params = {'orders':orders}
    return render(request, 'dashboard/orders.html', params)

def deleteOrder(request, id):
    order = Order.objects.get(id = id )
    order.delete()

    messages.success(request, 'Order deleted')
    return redirect('/dashboard/orders')

# products Management
@login_required(login_url = '/dashboard/admin-login')
@check_admin_account()
def productsList(request):
    if request.user.is_authenticated:
        products = Product.objects.all().order_by('-id')

        params = {'products':products}
        return render(request, 'dashboard/product.html', params)
    return redirect('adminLogin')   

    
def addNewProduct(request):
    if request.method == 'POST':
        name = request.POST['name'] 
        price = request.POST['price'] 
        unit = request.POST['unit'] 
        description = request.POST['description'] 
        image = request.FILES['image'] 

        product = Product(name = name, price = price, unit= unit, image= image, description= description)
        product.save()
        messages.success(request, 'Product added')
        return redirect('/dashboard/product')     
    return redirect('/dashboard/product')

def updateProduct(request, id):
    product  = Product.objects.get(id = id )
    product.name = request.POST['name']
    product.price = request.POST['price']
    product.unit = request.POST['unit']
    product.description = request.POST['description']

    product.save()
    messages.success(request, 'Products updated')
    return redirect('/dashboard/product')

def deletProduct(request, id):
    product  = Product.objects.get(id = id )
    product.delete()

    messages.success(request, 'Products deleted')
    return redirect('/dashboard/product')
