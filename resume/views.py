from django.shortcuts import render, redirect
from django.views import View
from resume.models import Resume
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.


class ResumesView(View):
    template_name = "resume/resumes.html"

    def get(self, request, *args, **kwargs):
        resumes = Resume.objects.all()

        return render(request, self.template_name, {"resumes": resumes})


class NewResumeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'resume/new_resume.html')

    def post(self, request, *args, **kwargs):
        resume_description = request.POST['description']
        current_id = request.user.id
        user_id = User.objects.get(id=current_id)
        if user_id.is_staff == 0:
            new_resume = Resume.objects.create(description=resume_description, author=user_id)
            return redirect('/home')
        else:
            return HttpResponse(status=403)
