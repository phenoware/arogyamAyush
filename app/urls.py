from django.urls import path,  re_path, include
from .import views
# from .views import Payment_Request,Payment_Response

urlpatterns = [
    path('',views.home, name='home'),
    ]