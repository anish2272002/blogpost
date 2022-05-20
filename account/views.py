from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .forms import UserProfile,UserForm,UserProfileForm,LoginForm
from uuid import uuid4
from datetime import datetime

def token_generator(usrname):
    t1=str(uuid4())
    t2=str(hash(usrname))
    t3=str(hash(str(datetime.now())))
    return (t1+t2+t3,datetime.now())

def signup(request):
    if(request.method=='POST'):
        usrdata=UserForm(request.POST)
        usrprofiledata=UserProfileForm(request.POST,request.FILES)
        if(usrdata.is_valid() and usrprofiledata.is_valid()):
            user=usrdata.save()
            user.set_password(user.password)
            user.is_active=False
            user.save()
            userprofile=usrprofiledata.save(commit=False)
            userprofile.user=user
            userprofile.token,userprofile.validatetime=token_generator(user.username)
            if(request.is_secure()):
                token='https://'+request.get_host()+'/account/'+userprofile.token
            else:
                token='http://'+request.get_host()+'/account/'+userprofile.token
            userprofile.save()
            msg="Hi {}\nHere is your account confirmation link:\n".format(user.first_name)+token
            send_mail("Account confirmation Mail",msg,settings.EMAIL_HOST_USER,[user.email])
            return render(request,'email_token.html',{'email':user.email})
    else:
        print(request.get_host(),request.is_secure())
        usrdata=UserForm()
        usrprofiledata=UserProfileForm()
    return render(request,'sign.html',{'userform':usrdata,'userprofileform':usrprofiledata})

def validate(request,slug):
    obj=get_object_or_404(UserProfile,token=slug)
    if(obj.user.is_active):
        return HttpResponseRedirect(reverse('account:login'))
    elif((datetime.now()-obj.validatetime).total_seconds()<2000):
        obj.user.is_active=True
        obj.user.save()
        return render(request,"validated.html",{'activated':True,'username':obj.user.username})
    else:
        obj.user.delete()
        return render(request,"validated.html",{'activated':False,'username':None})

class LoginView(View):
    form_class = LoginForm
    # Initial data
    initial = {}
    template_name = 'login.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            usr=form.cleaned_data['user']
            login(request,usr)
            return HttpResponseRedirect(reverse('blog:index'))
        return render(request, self.template_name, {'form': form})
