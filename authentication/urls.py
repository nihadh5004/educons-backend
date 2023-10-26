from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.Signup.as_view(), name ='signup'),
    path('logout/', views.Signout.as_view(), name ='logout'),
    # path('activate/', views.Activate.as_view(), name ='logout'),
    path('activate/<uidb64>/<token>', views.activate ,name='activate'),
    path('forgot-password/', views.ForgetPasswordEmailView.as_view(), name='forget_password'),
    path('reset-password/', views.ResetPassword.as_view(), name='reset-password'),
    path('forgot_password_mail/<str:uidb64>/<str:token>/', views.forgot_password_mail_view, name='forgot_password_mail'),

]
