from django.urls import path
from .import views

urlpatterns = [


    # Partner authentication process
    path('member-login/',views.memberLogin, name='memberLogin'),
    path('member-logout/',views.memberLogout, name='memberLogout'),
    path('member-register/',views.memberRegister, name='memberRegister'),
    path('member-under-review/',views.memberUnderReview, name='memberUnderReview'),

    # Paasword Reset Operation 
    path('get-email-address/',views.getEmailAddress, name='getEmailAddress'),
    path('verify-email/',views.vefiryEmail, name='vefiryEmail'),
    path('create-password/',views.createPassword, name='createPassword'),
    
    
    
    
    path('',views.home, name='home'),

    # refer user management     
    path('members/',views.members, name='members'),
    path('member-details/<str:phone>',views.memberDetails, name='membersDetails'),

    # Withdraw Request Management
    path('withdraw-request/',views.withdrawRequest, name='withdrawRequest'),
    path('create-withdraw-request/',views.createWithdrawRequest, name='createWithdrawRequest'),
    path('delete-request/<int:id>',views.deleteRequest, name='deleteRequest'),
    path('transacations/',views.transacations, name='transacations'),
    
    # Manage Account
    path('my-account/',views.myAccount, name='myAccount'),
    path('update-my-account/',views.updateMyAccount, name='updateMyAccount'),
    
    
    
    path('help/',views.help, name='help'),
    path('support/',views.support, name='support'),

    path('mark-as-read/',views.markAsRead, name='markAsRead'),
    

    
    

#     path('add-new-user/',views.addNewUser, name='addNewUser'),
#     path('user-details/<int:id>/',views.userDetails, name='userDetails'),

#     # History  
#     path('bidding-history/',views.biddingHistory, name='biddingHistory'),
#     path('jodi-bidding-history/',views.jodiBiddingHistory, name='jodiBiddingHistory'),

#     # withdraw request  
#     path('withdraw-request/',views.withdrawRequest, name='withdrawRequest'),
#     path('new-withdraw-request/',views.newWithdrawRequest, name='newWithdrawRequest'),

#     # Transfer Wallet 
#     path('transfer-wallet/<int:id>',views.transferWallet, name='transferWallet'),

]