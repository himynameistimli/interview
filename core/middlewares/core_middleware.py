from django.shortcuts import redirect
from django.urls import reverse, resolve


class RedirectMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        current_user = request.user
        path = request.path
        login_url = reverse('accounts:login')
        # admin_index = reverse('admin:index')
        if not current_user.is_authenticated and path not in [login_url]:
            # pass
            return redirect(login_url)

        if current_user.is_authenticated and path in [login_url, ]:
            return redirect('emart_mgmt:product_list')

        return self.get_response(request)
