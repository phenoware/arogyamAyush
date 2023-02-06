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
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout 
from django.db.models import Sum
import json
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from pattiMallProj.decorators import check_dealer_account
# Create your views here.

# HTML Mail Requirement stuff
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 
from django.utils.html import strip_tags



# User Authentication Views
def memberLogin(request):
    if request.method == 'POST':
        # get login details 
        username = request.POST['username'] 
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'Login Sucessfull')
            return redirect('/partner')
        else:
            messages.success(request,'Invalid Credentials')
            return redirect('/partner/member-login') 
    return render(request, 'partner/login.html')

def memberRegister(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        sponsoredId = request.POST['sponsoredId']
        productId = request.POST['productId']

        # check email aready exists
        if User.objects.filter(email = email).exists():
            messages.success(request, 'Email address already exists with us.')
            return redirect('/partner/member-register')
        print('\nEmail not exit')

        # Check phone number already exists
        if Dealer.objects.filter(phone = phone).exists():
            messages.success(request, 'Phone number already exists with us.')
            return redirect('/partner/member-register')
        print('\nNumber already not exites')

        # Check dealer exists as a sponsored
        if Dealer.objects.filter(phone = sponsoredId).exists():
            dealer = Dealer.objects.get(phone = sponsoredId)
            print('\nSponsored exites : '+str(dealer))
        else:
            messages.success(request, 'Please enter valid sponsored Id .')
            return redirect('/partner/member-register')
            
        

        # Create new user here 
        newUser = User.objects.create_user(username=email, email=email, password=password, first_name = name)
        newUser.save()
        print('\nNew User Account Created : ')
        user = User.objects.get(email = email)
        product = Product.objects.get(id = productId)

        # Create New Dealer Account
        dealer = Dealer(user = user, product = product, phone= phone, sponseredId = sponsoredId ,password = password, pins = 10, date = datetime.datetime.now(), walletBalance = 0 , paidBalance = 0 , pendingBalance = 0 , status = 'under-review', remark= 'Account under review')
        dealer.save()
        print('\nDealer Account Created : ')

        # Create Admin Notification 
        dealerAc = Dealer.objects.get(phone = phone)
        link = '/dashboard/members/under-review'
        adminNotification = AdminNotifications (status = 'new', msg = 'New user registration - Under Review' , date = datetime.datetime.now(), link = link)
        adminNotification.save() 
        
        # Create destributor account
        refDealer = Dealer.objects.get(phone = sponsoredId)
        distributor = Distributor(dealer = refDealer, product =  product, phone = phone, sponseredId = sponsoredId, date= datetime.datetime.now(), name= name, email = email)
        distributor.save()
        print('\nDistributor Account Created : ')

        messages.success(request, 'Account under review')
        return redirect('/partner/member-under-review')

        

    products = Product.objects.all()
    return render(request,'partner/register.html', {'products':products})

def memberUnderReview(request):
    return render(request, 'partner/under-review.html')

def getEmailAddress(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = random.randint(0000, 9999)
        
        if User.objects.filter(email = email).exists():
            u = User.objects.get(email = email)
            if Dealer.objects.filter(user_id = u.id).exists():
                # Send OTP mail to member
                subject = 'Password reset OTP - Arogyam Ayush'
                message = f'Your member account password reset six digit OTP is :{otp}.\n\nKindly note that do not share this OTP with anyone.'
                    
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,'phenoware@gmail.com']
                send_mail( subject, message, email_from, recipient_list )

                request.session['email'] = email
                request.session['otp'] = otp
                return redirect('/partner/verify-email/')
            else:
                messages.success(request, 'Please enter valid email.')
                return redirect('/partner/get-email-address/')
        else:
            messages.success(request, 'Please enter valid email.')
            return redirect('/partner/get-email-address/')

    return render(request, 'partner/get-email-address.html')

def vefiryEmail(request):
    if request.method == 'POST':
        one = request.POST['one'] 
        two = request.POST['two'] 
        three = request.POST['three'] 
        four = request.POST['four']
        
        otp = request.session.get('otp')
        email = request.session.get('email')
        enteredOtp = one + two + three + four

        if str(otp) == str(enteredOtp):

            return redirect('/partner/create-password/')  

        messages.success(request, 'Please enter valid OTP')    
        return redirect('/partner/verify-email/') 

    email = request.session.get('email')
    return render(request, 'partner/verify-email.html', {'email':email})

def createPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        email = request.session.get('email')

        u = User.objects.get( username=email )
        u.set_password(password)
        u.save()

        # delete Old Session 
        del request.session['email']
        del request.session['otp']

        messages.success(request, 'Password has been changed, Login with new password.')
        return redirect('/partner/member-login/') 
    return render(request, 'partner/create-password.html')


def memberLogout(request):
    logout(request)
    messages.success(request,'Logout')
    return redirect('/partner/member-login')


@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def home(request):
    member = Dealer.objects.get(user_id = request.user.id)
    id = member.id
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


    # Recent Joint Members 
    recentMembers = Distributor.objects.filter(dealer_id = member.id, status = 'under-review').order_by('-id')

    # Get member notifications 
    notifications = UserNotifications.objects.filter(dealer_id = id)
    notificationsCount = UserNotifications.objects.filter(dealer_id = id).count()

    params = {'member':member, 'directMembers':directMembers, 'directMembersCount':directMembersCount, 'level1':level1, 'level2':level2, 'level3':level3, 'level4':level4, 'level5':level5, 'totalMember':totalMember, 'totalRevenue':totalRevenue, 'walletBalance':walletBalance, 'recentMembers':recentMembers, 'notifications':notifications, 'notificationsCount':notificationsCount}
    return render(request, 'partner/index.html', params)



# Member management
@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def members(request):
    member = Dealer.objects.get(user_id = request.user.id)
    directMembers = Distributor.objects.filter(dealer_id = member.id, status = 'approved')

    params = {'directMembers':directMembers, 'member':member}
    return render(request, 'partner/members.html', params)

@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def memberDetails(request, phone):
    member = Dealer.objects.get(phone = phone)
    directMembers = Distributor.objects.filter(dealer_id = member.id, status= 'approved').order_by('-id')
    directMembersCount = Distributor.objects.filter(dealer_id = member.id, status= 'approved').count()

    params = {'member':member, 'directMembers':directMembers, 'directMembersCount':directMembersCount, 'phone':phone}
    return render(request, 'partner/member-details.html', params) 


# With Request Management
@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def withdrawRequest(request):
    member = Dealer.objects.get(user_id = request.user.id)
    withdrawRequest = Transaction.objects.filter(dealer_id = member.id).order_by('-id')

    params = {'withdrawRequest':withdrawRequest, 'member':member}
    return render(request, 'partner/withdraw-request.html', params)

@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def createWithdrawRequest(request):
    member = Dealer.objects.get(user_id = request.user.id)
    amount = request.POST['amount']
    
    if int(amount) <= int(member.walletBalance):
        transacation = Transaction(dealer = member, requestAmount = amount, requestDate = datetime.datetime.now(), status = 'unpaid')
        transacation.save()
        messages.success(request, 'New withdraw request created.')
        return redirect('/partner/withdraw-request') 
    else:
        messages.success(request, 'Withdraw amount must be less then wallet balance')
        return redirect('/partner/withdraw-request')

@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def deleteRequest(request, id ):
    req = Transaction.objects.get(id = id )
    req.delete()
    
    messages.success(request, 'Request Deleted')
    return redirect('/partner/withdraw-request')

@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def transacations(request):
    member = Dealer.objects.get(user_id = request.user.id)
    transactions = Transaction.objects.filter(dealer_id = member.id, status = 'approved').order_by('-id')

    params = {'transactions':transactions, 'member':member}
    return render(request, 'partner/transacations.html', params)

@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def myAccount(request):
    member = Dealer.objects.get(user_id = request.user.id)
    directMembers = Distributor.objects.filter(dealer_id = member.id, status= 'approved').order_by('-id')
    directMembersCount = Distributor.objects.filter(dealer_id = member.id, status= 'approved').count()

    params = {'member':member, 'directMembers':directMembers, 'directMembersCount':directMembersCount}
    return render(request, 'partner/my-account.html', params)

@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def updateMyAccount(request):
    user = User.objects.get(id = request.user.id)
    user.first_name = request.POST['name']
    user.save()

    member = Dealer.objects.get(user_id = request.user.id)
    member.bankName = request.POST['bankName']
    member.ifscCode = request.POST['ifscCode']
    member.accountNumber = request.POST['accountNumber']
    member.save()

    messages.success(request, 'Account updated')
    return redirect('/partner/my-account')

def help(request):
    return render(request, 'partner/help.html')

@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def support(request):
    if request.method == 'POST':
        member = Dealer.objects.get(user_id = request.user.id)
        phone = member.phone
        email = request.user.email 
        name = request.user.first_name
        subject = request.POST['subject']
        msg = request.POST['msg']
        date = datetime.datetime.now()

        inbox = Inbox(email = email, phone = phone, name= name, subject= subject, msg= msg, date = date, status = 'new')
        inbox.save()

        # Create Admin Notification
        notifiation = AdminNotifications(status = 'new', msg= 'New support ticket received from member panel', date= date, link = '/dashboard/messages/')
        notifiation.save()

        messages.success(request, 'Support message submitted, Our team will contact you shortly.')
        return redirect('/partner/support/')
    return render(request, 'partner/support.html')

@login_required(login_url = '/partner/member-login')
@check_dealer_account()
def markAsRead(request):
    member = Dealer.objects.get(user_id = request.user.id)
    notifiation = UserNotifications.objects.filter(dealer_id = member.id)

    for i in notifiation:
        i.status = 'seen'
        i.save()

    messages.success(request, 'All notifications are marked as read')
    return redirect('/partner')