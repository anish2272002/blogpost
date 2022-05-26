from django.urls import path
from .views import IndexView,UserBlogView

app_name='blog'

urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('userblogs',UserBlogView.as_view(),name='userblogs')
]