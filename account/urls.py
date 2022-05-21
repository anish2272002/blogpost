from django.urls import path
from .views import AccdetailView,LogoutView,signup,LoginView,validate

app_name='account'

urlpatterns = [
    path('sign',signup,name='sign'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('accdetail',AccdetailView.as_view(),name='accdetail'),
    path('<slug:slug>',validate,name='validate'),
]