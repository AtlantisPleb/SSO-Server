from django.urls import path
from . import views

urlpatterns = [
    path('authorize/', views.authorize, name='oidc_authorize'),
]