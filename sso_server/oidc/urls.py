from django.urls import path
from . import views

urlpatterns = [
    path('authorize/', views.authorize, name='oidc_authorize'),
    path('token/', views.token, name='oidc_token'),
    path('userinfo/', views.userinfo, name='oidc_userinfo'),
]