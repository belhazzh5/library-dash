from django.db import models
from django.contrib.auth.models import User
import uuid 
from django.utils.text import slugify
from django.urls import reverse
from datetime import date, datetime

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    date_birth = models.DateField(blank=True, null=True)
    date_death = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='images/authors/',blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("author", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
       if not self.slug:
        self.slug = slugify(self.name)
       super(Author, self).save(*args, **kwargs) # Call the real save() method   

class Book(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    author = models.ForeignKey(Author, related_name='writter', on_delete=models.SET_NULL,null=True)
    summary = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True,default=25.5)
    isbn = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/books/',blank=True, null=True)
    genre = models.ManyToManyField(Genre,related_name="my_book")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL,null=True)
    def save(self, *args, **kwargs):
       if not self.slug:
        self.slug = slugify(self.title)
       super(Book, self).save(*args, **kwargs) # Call the real save() method
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("book", kwargs={"slug": self.slug})
        
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ' '.join(genre.name for genre in self.genre.all()[:3])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    due_back = models.DateField()
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='borrower', on_delete=models.SET_NULL, null=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)
    def save(self, *args, **kwargs):
        if self.status == 'm' or self.status == 'a':
            self.status = 'o'
        super(BookInstance, self).save(*args, **kwargs) # Call the real save() method
    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)

class SingleBlog(models.Model):
    title = models.CharField(max_length=50,blank=True, null=True,default=" ")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/blogs/%d-%m-%y/',blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title or "no-title"


class Blog(models.Model):
    title = models.CharField(max_length=50,blank=True, null=True,default=" ")
    image = models.ImageField(upload_to='images/blogs/%d-%m-%y/',blank=True, null=True)
    blogs = models.ManyToManyField('SingleBlog')
    slug = models.SlugField(blank=True, null=True)
    date = models.DateField(auto_now_add=True,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    def save(self, *args, **kwargs):
       if not self.slug:
        self.slug = slugify(self.title)
       super(Blog, self).save(*args, **kwargs) # Call the real save() method
    def get_absolute_url(self):
        return reverse("blog", kwargs={"slug": self.slug})
    def __str__(self):
        return self.title or "no title"
    
class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254,blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return self.name
    def has_been(self):
        if self.date:
            return (datetime.now() - self.date)

class Adress(models.Model):
    street = models.CharField(max_length=50,blank=True, null=True)
    city = models.CharField(max_length=50,blank=True, null=True)
    state = models.CharField(max_length=50,blank=True, null=True)
    def __str__(self):
        return self.state

class Skill(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True)
    power = models.IntegerField(blank=True, null=True,default=50)
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    email = models.EmailField(max_length=254,blank=True, null=True)
    image = models.ImageField(upload_to="images/users/",default="images/user.png")
    website = models.URLField(max_length=200,blank=True, null=True)
    adresse = models.ForeignKey(Adress, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=50,blank=True, null=True)
    nikname = models.CharField(max_length=50,blank=True, null=True)
    skills = models.ManyToManyField(Skill)
    def __str__(self):
        return str(self.name)
    
class Activity(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return self.user.username
