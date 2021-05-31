from django.contrib.auth import authenticate, login
from django.urls import reverse

from core import core_lib
from accounts import forms as accounts_form


def customer_login_handler(request):
    errors = dict()
    errors['__all__'] = list()
    try:
        form = accounts_form.LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            # do some stuffs based on user_type

            login(request, user)
            if not user:
                errors['__all__'].append('Wrong username or password')
                return core_lib.return_multi_key_json_response(['errors'], [errors])
            else:
                success_url = reverse('emart_mgmt:product_list')
                return core_lib.return_multi_key_json_response(['success', 'success_url'],
                                                               [True, success_url])

        else:
            return core_lib.return_multi_key_json_response(['errors'], [form.errors])

    except Exception as ex:
        return core_lib.handle_exception(print_exception=True, http_response=True,
                                         raise_exception=True)
