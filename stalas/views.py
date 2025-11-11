from django.contrib.auth import login
from django.views.generic import TemplateView

from stalas.forms import SignupForm, LoginForm
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect


class WrongAnswerView(TemplateView):
    template_name = 'debilas.html'


class HomeView(TemplateView):
    template_name = 'home.html'


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm

    def form_valid(self, form):
        baudejas = form.save(commit=True)

        login(self.request, baudejas)

        if self.request.headers.get('HX-Request'):
            return render(self.request, 'signup_success.html', {'user': baudejas})

        return super().form_valid(form)

    def form_invalid(self, form):
        if "__all__" in form.errors or "dating_status" in form.errors or "favourite_colour" in form.errors:
            return redirect(reverse("debilas"))
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.user)
        return redirect('home')