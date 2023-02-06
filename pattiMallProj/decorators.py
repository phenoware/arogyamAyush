from functools import wraps
from django.http import HttpResponseRedirect, HttpResponse
from dashboard.models import Dealer, Distributor, Transaction, Product, Order, Inbox , AdminNotifications, AdminNotifications
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render,redirect

def check_admin_account():
    def decorator(view_func):
        @wraps(view_func)
        def _is_logged_in(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_superuser == 1:
                    return view_func(request, *args, **kwargs)
                else:
                    logout(request)
                    messages.success(request, 'Yor are not authorised to access admin panel.')
                    return HttpResponseRedirect('/dashboard/admin-login')

            else:
                return view_func(request, *args, **kwargs)
        return _is_logged_in
    return decorator

def check_dealer_account():
    def decorator(view_func):
        @wraps(view_func)
        def _is_logged_in(request, *args, **kwargs):
            if request.user.is_authenticated:
                if Dealer.objects.filter(user_id = request.user.id).exists():
                    dealer = Dealer.objects.get(user_id = request.user.id)
                    if dealer.status == 'approved':
                        return view_func(request, *args, **kwargs)
                    else:
                        messages.success(request, 'Account under review')
                        return redirect('/partner/member-under-review')
                else:
                    logout(request)
                    messages.success(request, 'Yor are not authorised to access broker panel, Please contact with admin')
                    return HttpResponseRedirect('/partner/member-login')

            else:
                return view_func(request, *args, **kwargs)
        return _is_logged_in
    return decorator
