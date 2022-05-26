from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Blog

class IndexView(ListView):
    model = Blog
    template_name = 'index.html'
    context_object_name = 'blogs'
    queryset = Blog.objects.all().order_by('-datetime')[:10]

class UserBlogView(ListView):
    model = Blog
    template_name = 'userblogs.html'
    context_object_name = 'userblogs'
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,
            {self.context_object_name:Blog.objects.filter(blogger=request.user).order_by('-datetime')})