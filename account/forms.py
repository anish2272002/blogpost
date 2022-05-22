from dataclasses import fields
from django import forms
from .models import User,UserProfile
from django.contrib.auth import authenticate

class UserForm(forms.ModelForm):
    cpassword=forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    def clean(self):
        cleaned_data=super().clean()
        if(cleaned_data['password']!=cleaned_data['cpassword']):
            raise forms.ValidationError("Passwords do not match!")
    class Meta:
        model=User
        fields=('username','password','cpassword','first_name','last_name','email')
        labels={
            'username':'',
            'password':'',
            'first_name':'',
            'last_name':'',
            'email':'',
        }
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'})
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('first_name','last_name','email')
        labels={
            'first_name':'',
            'last_name':'',
            'email':'',
        }
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'})
        }
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=('dob','profile_pic')
        labels={
            'dob':'',
            'profile_pic':''
        }
        widgets={
            'dob':forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Date of Birth','type': 'date'}),
            'profile_pic':forms.FileInput(attrs={'class':'form-control'})
        }

class LoginForm(forms.Form):
    username=forms.CharField(max_length=256,label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password=forms.CharField(max_length=256,label='',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    def clean(self):
        super().clean()
        usr=authenticate(username=self.cleaned_data['username'],password=self.cleaned_data['password'])
        if(usr and usr.is_active):
            self.cleaned_data['user']=usr
        else:
            if(usr):
                usr.delete()
            raise forms.ValidationError("Incorrect Username/Password")