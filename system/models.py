from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True,upload_to="images/category")
    def __str__(self):
        return self.name
    
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=8,blank=True, null=True)
    photo = models.ImageField(upload_to="images/instructor")
    address = models.CharField(max_length=100,blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
       if not self.slug:
            self.slug = slugify(self.user.username)
       super(Instructor, self).save(*args, **kwargs) # Call the real save() method

class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,blank=True, null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    photo = models.ImageField(blank=True, null=True,upload_to="images/course")
    price = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True,blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs) # Call the real save() method

class Quizz(models.Model):
    title = models.CharField(max_length=50)
    question = models.CharField(max_length=100)
    answer1 = models.CharField(max_length=100)
    answer2 = models.CharField(max_length=100)
    answer3 = models.CharField(max_length=100)
    answer4 = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True,blank=True, null=True)
    correct_answer = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Quizz, self).save(*args, **kwargs) # Call the real save() method   

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100,blank=True, null=True)
    photo = models.ImageField(blank=True, null=True,upload_to="images/student")
    slug = models.SlugField(blank=True, null=True)
    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Student, self).save(*args, **kwargs) # Call the real save() method        

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course)
    score = models.IntegerField(blank=True, null=True,default=0)
    percentage = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.student.user.username

    