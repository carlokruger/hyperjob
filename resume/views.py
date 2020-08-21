from django.shortcuts import render
from django.views import View
from resume.models import Resume

# Create your views here.

class ResumesView(View):
    template_name = "resume/resumes.html"

    def get(self, request, *args, **kwargs):
        resumes = Resume.objects.all()

        return render(request, self.template_name, {"resumes": resumes})
