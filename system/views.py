from django.shortcuts import render
from .models import Course
from .forms import CourseForm
from django.views.generic.edit import CreateView
from django.http import JsonResponse
# Create your views here.
def home(request):
    return render(request, "system/index.html")
def page(request):
    dates = []
    courses = Course.objects.all()
    all_courses = Course.objects.all().count()
    front = Course.objects.filter(category__name="FrontEnd").count()
    back = Course.objects.filter(category__name="BackEnd").count()
    aws = Course.objects.filter(category__name="aws").count()
    cloud = Course.objects.filter(category__name="cloud").count()
    agile = Course.objects.filter(category__name="agile").count()
    for c in courses:
        dates.append(c.date.month)
    context = {
        'months':dates,
        'front':front,
        'back':back,
        'agile':agile,
        "aws":aws,
        'cloud':cloud,
    }
    return render(request, "system/charts-apexcharts.html",context)

def index(request):
    courses = Course.objects.all()
    context = {
        'courses':courses,
        'nbCourses': Course.objects.all().count(),
    }    
    return render(request, "system/components-cards.html",context)
    # return JsonResponse(context)

class CourseCreateView(CreateView):
    form_class = CourseForm
    fields = '__all__'
    template_name = "system/forms-elements.html"
    success_url = "/"




def error_404_view(request, exception):
   
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')