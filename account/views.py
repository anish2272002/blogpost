from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.conf import settings
from django.core.mail import send_mail
from uuid import uuid4
from datetime import datetime
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout

from .forms import User,UserProfile,UserForm,UserUpdateForm,UserProfileForm,LoginForm

class SignupView(View):
    template_name = 'sign.html'
    template_name_email = 'email_token.html'
    def token_generator(self,usrname):
        t1=str(uuid4())
        t2=str(hash(usrname))
        t3=str(hash(str(datetime.now())))
        return t1+t2+t3
    def get(self,request,*args,**kwargs):
        usrdata=UserForm()
        usrprofiledata=UserProfileForm()
        return render(request,self.template_name,{'userform':usrdata,'userprofileform':usrprofiledata})
    def post(self,request,*args,**kwargs):
        usrdata=UserForm(request.POST)
        usrprofiledata=UserProfileForm(request.POST,request.FILES)
        if(usrdata.is_valid() and usrprofiledata.is_valid()):
            user=usrdata.save()
            user.set_password(user.password)
            user.is_active=False
            user.save()
            userprofile=usrprofiledata.save(commit=False)
            userprofile.user=user
            userprofile.token=self.token_generator(user.username)
            userprofile.validatetime=datetime.now()
            if(request.is_secure()):
                token='https://'+request.get_host()+'/account/'+userprofile.token
            else:
                token='http://'+request.get_host()+'/account/'+userprofile.token
            userprofile.save()
            msg="Hi {0}\nHere is your account confirmation link:\n{1}\nTeam Diary\n".format(user.first_name,token)
            send_mail("Account confirmation Mail",msg,settings.EMAIL_HOST_USER,[user.email])
            return render(request,self.template_name_email,{'email':user.email})
        else:
            return render(request,self.template_name,{'userform':usrdata,'userprofileform':usrprofiledata})

class ValidateView(View):
    template_name='validated.html'
    def get(self,request,slug):
        obj=get_object_or_404(UserProfile,token=slug)
        if(obj.user.is_active):
            return HttpResponseRedirect(reverse('account:login'))
        elif((datetime.now()-obj.validatetime).total_seconds()<2000):
            obj.user.is_active=True
            obj.user.save()
            return render(request,self.template_name,{'activated':True,'username':obj.user.username})
        else:
            obj.user.delete()
            return render(request,self.template_name,{'activated':False,'username':None})

class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            usr=form.cleaned_data['user']
            login(request,usr)
            return HttpResponseRedirect(reverse('blog:index'))
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('blog:index'))

class AccdetailView(View):
    template_name='accdetail.html'
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        # userprofile=get_object_or_404(UserProfile,pk=request.user)
        userupdateform = UserUpdateForm(instance=request.user)
        userprofileform = UserProfileForm(instance=request.user.profile)
        return render(request,self.template_name,{'userupdateform':userupdateform,'userprofileform':userprofileform})
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        userupdateform=UserUpdateForm(request.POST,instance=request.user)
        userprofileform=UserProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if(userupdateform.is_valid() and userprofileform.is_valid()):
            userupdateform.save()
            userprofileform.save()
        return render(request,self.template_name,{'userupdateform':userupdateform,'userprofileform':userprofileform})

class DeleteUserView(View):
    template_name='delete.html'
    @method_decorator(login_required)
    def get(self,request):
        return render(request,self.template_name)
    @method_decorator(login_required)
    def post(self,request):
        usr=request.user
        logout(request)
        usr.delete()
        return render(request,self.template_name)