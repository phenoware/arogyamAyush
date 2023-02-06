from django.urls import path
from .import views

urlpatterns = [


    path('paytmweb/',views.paytmweb, name='paytmweb'),
    path('handlerequestweb/',views.handlerequestweb, name='handlerequestweb'),
    path('payment-success-web/<str:successPaymentId>',views.paymentSuccessWeb, name='paymentSuccessWeb'),
    path('order-placed/',views.orderPlaced, name='orderPlaced'),
    
    path('',views.home, name='home'),
    path('shop/',views.shop, name='shop'),

    # Products URLS 
    path('product-details/<int:id>/',views.productDetails, name='productDetails'),

    # review
    path('submit-review/',views.submitReview, name='submitReview'),
    path('subsribe/',views.subsribe, name='subsribe'),
    
    path('checkout/',views.checkout, name='checkout'),
    path('place-order/',views.placeOrder, name='placeOrder'),


    path('about-us/',views.aboutUs, name='aboutUs'),
    path('contact/',views.contact, name='contact'),
    path('send-message/',views.sendMessage, name='sendMessage'),
    
    path('term-of-services/',views.termServices, name='termServices'),
    path('refund-policy/',views.refundPolicy, name='refundPolicy'),
    path('privacy-policy/',views.privacyPolicy, name='privacyPolicy'),

    path('upload-apk/',views.uploadApk, name='uploadApk'),
    path('make-upload-apk/',views.makeUpload, name='makeUpload'),
    
    
    
    path('result-panel/',views.resultPanel, name='resultPanel'),
    path('result-panel-chart/<int:id>',views.resultPanelChart, name='resultPanelChart'),

]