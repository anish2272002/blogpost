from django.urls import path
from .views import IndexView,UserBlogView,BlogView,CreateBlogView,DeleteBlogView,UpdateBlogView

app_name='blog'

urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('userblogs/<path:username>',UserBlogView.as_view(),name='userblogs'),
    path('blog/<int:pk>/<path:username>',BlogView.as_view(),name='blog'),
    path('blogdelete/<int:pk>',DeleteBlogView.as_view(),name='delete'),
    path('blogupdate/<int:pk>',UpdateBlogView.as_view(),name='update'),
    path('createblog',CreateBlogView.as_view(),name='createblog')
]