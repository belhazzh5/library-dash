from django.contrib import admin
from .models import (Course,Student,Instructor,Result,Quizz,Category)
# Register your models here.
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Result)
admin.site.register(Quizz)
admin.site.register(Category)