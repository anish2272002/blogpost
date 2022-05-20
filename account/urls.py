from django.urls import path
from .views import signup,LoginView,validate

app_name='account'

urlpatterns = [
    path('sign',signup,name='sign'),
    path('login',LoginView.as_view(),name='login'),
    path('<slug:slug>',validate,name='validate')
]