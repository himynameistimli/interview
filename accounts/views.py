from django.contrib.auth.views import LoginView
from django.shortcuts import render

# Create your views here.
from django.views import View
from accounts import handlers as accounts_handlers


class CustomerLoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
        return accounts_handlers.customer_login_handler(request)
