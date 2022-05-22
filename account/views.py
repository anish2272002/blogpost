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
    def send_email(self,request,fname,dbtoken,email):
        if(request.is_secure()):
            token='https://'+request.get_host()+'/account/'+dbtoken
        else:
            token='http://'+request.get_host()+'/account/'+dbtoken
        msg="Hi {0}\nHere is your account confirmation link:\n{1}\nTeam Diary\n".format(fname,token)
        send_mail("Account confirmation Mail",msg,settings.EMAIL_HOST_USER,[email])
    def get(self,request,username,*args,**kwargs):
        if(username=='abc'):
            usrdata=UserForm()
            usrprofiledata=UserProfileForm()
            return render(request,self.template_name,{'userform':usrdata,'userprofileform':usrprofiledata})
        else:
            usr=get_object_or_404(User,username=username)
            if(usr.is_active):
                return HttpResponseRedirect(reverse('account:login'))
            else:
                usr.profile.validatetime=datetime.now()
                usr.save()
                self.send_email(request,usr.first_name,usr.profile.token,usr.email)
                return render(request,self.template_name_email,{'email':usr.email,'username':usr.username})
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
            userprofile.save()
            self.send_email(request,user.first_name,userprofile.token,user.email)
            return render(request,self.template_name_email,{'email':user.email,'username':user.username})
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
            usrname=obj.user.username
            obj.user.delete()
            return render(request,self.template_name,{'activated':False,'username':usrname})

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
        if(request.POST['username']==request.user.username):
            usr=request.user
            usrname=usr.username
            logout(request)
            usr.delete()
            return render(request,self.template_name,{'username':usrname})
        else:
            return HttpResponseRedirect(reverse('account:accdetail'))

class ForgotPasswordView(View):
    template_usr_name='forgotusr.html'
    template_pwd_name='forgotpwd.html'
    template_name='forgot.html'
    def token_generator(self,usrname):
        t1=str(uuid4())
        t2=str(hash(usrname))
        t3=str(hash(str(datetime.now())))
        return t1+t2+t3
    def send_email(self,request,usr):
        usrprofile=get_object_or_404(UserProfile,user=usr)
        usrprofile.token=self.token_generator(usr.username)
        usrprofile.validatetime=datetime.now()
        usrprofile.save()
        if(request.is_secure()):
                token='https://'+request.get_host()+'/account/forgot/'+usrprofile.token
        else:
            token='http://'+request.get_host()+'/account/forgot/0/'+usrprofile.token
        msg="Hi {0}\nHere is your password reset link:\n{1}\nTeam Diary\n".format(usr.first_name,token)
        send_mail("Password Reset Request Mail",msg,settings.EMAIL_HOST_USER,[usr.email])
    def get(self,request,getusername,slug):
        if(getusername):
            return render(request,self.template_usr_name)    
        else:
            obj=get_object_or_404(UserProfile,token=slug)
            if((datetime.now()-obj.validatetime).total_seconds()<2000):
                return render(request,self.template_pwd_name,{'username':obj.user.username})
            else:
                return render(request,self.template_name,{'expired':True})
    def post(self,request,getusername,slug):
        if(getusername):
            usr=get_object_or_404(User,username=request.POST['username'])
            self.send_email(request,usr)
            return render(request,self.template_name,{'expired':False,'email':usr.email})
        else:
            obj=get_object_or_404(UserProfile,token=slug)
            obj.user.password=request.POST['password']
            obj.user.set_password(obj.user.password)
            obj.user.save()
            return HttpResponseRedirect(reverse('account:login'))
