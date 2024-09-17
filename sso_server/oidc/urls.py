from django.urls import path
from . import views

urlpatterns = [
    path('authorize/', views.authorize, name='oidc_authorize'),
    path('token/', views.token, name='oidc_token'),
]