from django.contrib import admin
from .models import Author, Genre, Book, BookInstance,Language,SingleBlog,Blog,Message,Profile,Adress,Skill,Activity
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_birth', 'date_death')
    fields = ['name', ('date_birth', 'date_death')]


# Unfortunately we can't directly specify the genre field in list_display because it is a ManyToManyField (Django prevents this because there would be a large database access "cost" in doing so).
#  Instead we'll define a display_genre function to get the information as a string (this is the function we've called above; we'll define it below).

admin.site.register(Genre)
admin.site.register(Skill)
admin.site.register(Adress)
admin.site.register(Language)
admin.site.register(Blog)
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(SingleBlog)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','user','due_back')
    list_filter = ('status', 'due_back')

@admin.register(Activity)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('user','name')