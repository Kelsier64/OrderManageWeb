from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm
from .models import ExtendedUser
from django.contrib.auth.models import User
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    def form_valid(self, form):
        user = form.cleaned_data['user']
        login(self.request, user)
        try:
            extended_user = ExtendedUser.objects.get(user=user)
            if extended_user.user_class == 'op':
                return redirect('/op/')
            else:
                return redirect('/customer/')
        except ExtendedUser.DoesNotExist:
            form.add_error(None, 'Invalid user class')
            return self.form_invalid(form)
    

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/login/')

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/login')
    
