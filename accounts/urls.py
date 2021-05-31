from django.urls import path
from django.contrib.auth.views import LogoutView

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', views.CustomerLoginView.as_view(), name='login')
]
