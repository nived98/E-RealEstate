from django.urls import path
from blog.api.views import (
    registration_view,
    account_properties_view,
    update_account_view
)
from rest_framework.authtoken.views import obtain_auth_token
app_name = 'blog'

urlpatterns = [
    path('properties', account_properties_view, name='properties'),
    path('properties/update', update_account_view, name='update'),
    path('register', registration_view, name='register'),
    path('login', obtain_auth_token, name='login'),
]
