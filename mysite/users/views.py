from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import RegisterForm
from django.views import View


# Create your views here.

class LogoutView(View):
    # template_name =   'users/logout.html'

    def get(self, request):
        logout(request)
        return redirect(to="quotes:root")

class RegisterView(View):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotes:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created by {username}')
            return redirect(to="users:signin")
        return render(request, self.template_name, {'form': form})