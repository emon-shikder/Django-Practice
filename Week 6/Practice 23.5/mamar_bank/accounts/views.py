from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')


class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
    
    
class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "accounts/password_change.html"

    def get_success_url(self):
        message = render_to_string(
            "accounts/mail.html",
            {
                "user": self.request.user,
            },
        )
        to_email = [self.request.user.email]
        if isinstance(message, tuple):
            message = "".join(message)
        send_email = EmailMultiAlternatives(
            subject="Password Change",
            body="",
            to=to_email,
        )
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        return reverse_lazy("profile")

    def form_valid(self, form):
        messages.success(self.request, "Password Change Successful")
        return super().form_valid(form)