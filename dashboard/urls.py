from django.urls import path
from .import views

urlpatterns = [

    # User Authentication URL's
    path('admin-login/',views.adminLogin, name='adminLogin'),
    path('handle-admin-login/',views.handleAdminLogin, name='handleAdminLogin'),
    path('admin-logout/',views.adminLogout, name='adminLogout'),



    path('',views.home, name='home'),

    # Members Management 
    path('members/<str:status>',views.members, name='members'),
    path('member-details/<int:id>',views.memberDetails, name='memberDetails'),
    path('member-details-by-phone/<int:phone>',views.memberDetailsByPhone, name='memberDetailsByPhone'),
    path('delete-member/<int:id>',views.deleteMember, name='deleteMember'),
    path('approve-member/<int:id>',views.approveMember, name='approveMember'),

    
    # Financial Operations Here 
    path('transactions/',views.transactions, name='transactions'),
    path('withdraw-request/',views.withdrawRequest, name='withdrawRequest'),
    path('delete-request/<int:id>/',views.deleteRequest, name='deleteRequest'),
    path('approve-request/<int:id>',views.approveRequest, name='approveRequest'),
    

    # Manage Notifications 
    path('view-notifiation/<int:id>',views.viewNotification, name='viewNotification'),
    path('mark-as-read/',views.markAsRead, name='markAsRead'),
    
    

    
    path('messages/',views.msg, name='msg'),

    
    
    
    # Orders Management
    path('orders/',views.orders, name='orders'),
    path('delete-order/<int:id>',views.deleteOrder, name='deleteOrder'),
    
    
    # Product / Package Management 
    path('product/',views.productsList, name='productsList'),
    path('add-new-product/',views.addNewProduct, name='addNewProduct'),
    path('update-product/<int:id>/',views.updateProduct, name='updateProduct'),
    path('delete-product/<int:id>/',views.deletProduct, name='deletProduct'),

    
    

    
    ]