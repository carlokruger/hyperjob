from django.shortcuts import render, redirect
from django.views import View
from vacancy.models import Vacancy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

class IndexView(View):
    template_name = "vacancy/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class VacanciesView(View):
    template_name = "vacancy/vacancies.html"

    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()

        return render(request, self.template_name, {"vacancies": vacancies})


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'login.html'


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name, {"user": request.user.username, "userid": request.user.id, "staff": request.user.is_staff})
        else:
            return render(request, self.template_name, {"user": None})


class NewVacancyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'vacancy/new_vacancy.html')

    def post(self, request, *args, **kwargs):
        vacancy_description = request.POST['description']
        current_id = request.user.id
        user_id = User.objects.get(id=current_id)
        if user_id.is_staff == 1:
            new_vacancy = Vacancy.objects.create(description=vacancy_description, author=user_id)
            return redirect('/home')
        else:
            return HttpResponse(status=403)
