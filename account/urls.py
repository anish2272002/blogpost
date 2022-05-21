from django.urls import path
from .views import AccdetailView,LogoutView,SignupView,LoginView,DeleteUserView,ValidateView,ForgotPasswordView

app_name='account'

urlpatterns = [
    path('sign',SignupView.as_view(),name='sign'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('accdetail',AccdetailView.as_view(),name='accdetail'),
    path('delete',DeleteUserView.as_view(),name='delete'),
    path('forgot/<int:getusername>/<slug:slug>',ForgotPasswordView.as_view(),name='forgot'),
    path('<slug:slug>',ValidateView.as_view(),name='validate'),
]