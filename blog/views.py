from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .models import Blog,Comment
from .forms import CreateBlogForm

class IndexView(ListView):
    model = Blog
    template_name = 'index.html'
    context_object_name = 'objects'
    queryset = Blog.objects.all().order_by('-datetime')[:10]

class UserBlogView(ListView):
    model = Blog
    template_name = 'userblogs.html'
    context_object_name = 'userblogs'
    def get(self,request,username,*args,**kwargs):
        usr=get_object_or_404(User,username=username)
        return render(request,self.template_name,
            {self.context_object_name:Blog.objects.filter(blogger=usr).order_by('-datetime'),'userdetail':usr})

class BlogView(DetailView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blog'
    def get(self,request,pk,username,*args,**kwargs):
        usr=get_object_or_404(User,username=username)
        return render(request,self.template_name,{self.context_object_name:Blog.objects.get(id=pk),
                'otherblogs':Blog.objects.filter(blogger=usr).order_by('-datetime').exclude(id=pk)[:10],
                'comments':Comment.objects.filter(blog=Blog.objects.get(id=pk)).order_by('-datetime'),
                'current_time':datetime.now()})
    @method_decorator(login_required)
    def post(self,request,pk,username,*args,**kwargs):
        comment=Comment(blogger=request.user,blog=Blog.objects.get(id=pk),
            text=request.POST['comment'],datetime=datetime.now())
        comment.save()
        usr=get_object_or_404(User,username=username)
        return render(request,self.template_name,{self.context_object_name:Blog.objects.get(id=pk),
                'otherblogs':Blog.objects.filter(blogger=usr).order_by('-datetime').exclude(id=pk)[:10],
                'comments':Comment.objects.filter(blog=Blog.objects.get(id=pk)).order_by('-datetime'),
                'current_time':datetime.now()})

class CreateBlogView(View):
    template_name = "createblog.html"
    @method_decorator(login_required)
    def get(self,request):
        return render(request,self.template_name,{'form':CreateBlogForm()})
    @method_decorator(login_required)
    def post(self,request):
        form=CreateBlogForm(request.POST,request.FILES)
        if(form.is_valid()):
            obj=form.save(commit=False)
            obj.blogger=request.user
            obj.datetime=datetime.now()
            obj.image=form.cleaned_data['image']
            obj.save()
            return HttpResponseRedirect(reverse('blog:userblogs',kwargs={'username':request.user.username}))
        else:
            return render(request,self.template_name,{'form':form})

class UpdateBlogView(View):
    template_name = "updateblog.html"
    @method_decorator(login_required)
    def get(self,request,pk):
        blog=get_object_or_404(Blog,id=pk)
        return render(request,self.template_name,{'form':CreateBlogForm(instance=blog)})
    @method_decorator(login_required)
    def post(self,request,pk):
        blog=get_object_or_404(Blog,id=pk)
        form=CreateBlogForm(request.POST,request.FILES,instance=blog)
        if(form.is_valid()):
            obj=form.save(commit=False)
            obj.datetime=datetime.now()
            obj.save()
            return HttpResponseRedirect(reverse('blog:userblogs',kwargs={'username':request.user.username}))
        else:
            return render(request,self.template_name,{'form':form})

class DeleteBlogView(DeleteView):
    model=Blog
    context_object_name = 'blog'
    template_name = "deleteblog.html"
    success_url = reverse_lazy("blog:userblogs")
    @method_decorator(login_required)
    def post(self,request,pk):
        post=get_object_or_404(Blog,id=pk)
        if(post.blogger.username==request.user.username and post.title==request.POST["blog_title"]):
            post.delete()
        return HttpResponseRedirect(reverse("blog:userblogs",kwargs={'username':request.user.username}))