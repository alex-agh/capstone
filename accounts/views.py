from allauth.account.views import SignupView
from django.shortcuts import render

def signup(request):
    return SignupView.as_view()(request)