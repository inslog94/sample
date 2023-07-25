from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm


class Signup(View):
    def get(self, req):
        if req.user.is_authenticated:
            print("이미 로그인됨")
            return redirect('blog:list')
        
        form = SignupForm()
        print("form", form)
        context = {
            "form": form
        }
        return render(req, 'user/user_signup.html', context)
    
    def post(self, req):
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save()
            
            return redirect('user:login')
        
        context = {
            "form": form
        }
        return render(req, 'user/user_signup.html', context)


class Login(View):
    def get(self, req):
        print("로그인 여부", req.user.is_authenticated)
        if req.user.is_authenticated:
            print("이미 로그인됨")
            return redirect('blog:list')
        
        form = LoginForm()
        context = {
            "form": form
        }
        
        return render(req, 'user/user_login.html', context)

    def post(self, req):
        if req.user.is_authenticated:
            print("이미 로그인됨")
            return redirect('blog:list')
        
        form = LoginForm(req, req.POST)
        print("폼 체크", form, form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print("로그인 체크", user)
            
            if user:
                login(req, user)
                return redirect('blog:list')
        
        # print("로그인 실패", form)
        context = {
            "form": form
        }
        
        return render(req, 'user/user_login.html', context)


class Logout(View):
    def get(self, req):
        logout(req)
        return redirect('user:login')