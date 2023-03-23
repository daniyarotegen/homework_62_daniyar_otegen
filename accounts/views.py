from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView
from accounts.forms import LoginForm, CustomUserCreationForm


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        context['register_url'] = reverse('register')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            messages.error(request, 'Invalid data')
            return redirect('index')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.warning(request, 'User is not found')
            return redirect('index')
        login(request, user)
        messages.success(request, 'Welcome')
        next_request = request.GET.get('next')
        if next_request:
            return redirect(next_request)
        return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = 'index'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(self.success_url)
        context = {'form': form}
        context['login_url'] = reverse('login')
        return self.render_to_response(context)

