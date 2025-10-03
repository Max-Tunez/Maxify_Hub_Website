from django.urls import path
from authapp import views
from .views import *

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.handleLogin,name="handleLogin"),
    path('logout/',views.handleLogout,name="handleLogout"),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(), name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>/',views.SetNewPasswordView.as_view(),name='set-new-password'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),
    path('paystack-webhook/', views.paystack_webhook, name='paystack_webhook'),
]