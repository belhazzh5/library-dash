from django.shortcuts import render,redirect,get_object_or_404
from .models import Book, Author, BookInstance, Genre,Blog,Message,Profile,Activity
from django.views.generic import ListView,DetailView
from django.db.models import Q
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import BookSerializer
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RenewBookForm,AuthorForm,BookForm,BookInstanceForm,UserRegisterForm,ProfileForm
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from datetime import timedelta
import math
from django.core.exceptions import PermissionDenied

# Create your views here.

def home(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    blogs = Blog.objects.all()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'blogs': blogs,
    }
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            if not request.user.is_authenticated:
                name = request.POST.get('name')
                email = request.POST.get('email')
            else:
                name = request.user.username
                email = request.user.email or "no email for this user"
            Message.objects.create(name=name,message=message,email=email)
            return HttpResponseRedirect(reverse('catalog'))
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalogue/index.html', context=context)

class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    template_name = 'catalogue/book_list.html'  # Specify your own template name/location
    paginate_by = 6
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            query = self.request.GET.get('query')
            if query:
                context['book_list'] = Book.objects.filter(
                                    Q(title__icontains=query) | 
                                    Q(genre__name__icontains=query)
                ).distinct()
        context["genres"] = Genre.objects.all()
        context["genre"] = Genre.objects.first()
        return context
    
class BookDetailView(DetailView):
    model = Book
    template_name = "catalog/book.html"
    
class AuthorListView(LoginRequiredMixin,ListView):
    model = Author
    template_name = "catalog/authors.html"
    context_object_name = 'author_list'

class AuthorDetailView(DetailView):
    model = Author
    template_name = "catalog/author.html"
    context_object_name = 'author'

class LoanedBooksByUserListView(LoginRequiredMixin,ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalogue/bookinstance_list_borrowed_user.html'
    context_object_name = 'myBooks'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(user=self.request.user).filter().order_by('due_back')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expenses = 0
        for book in context['myBooks']:
            expenses += book.book.price
        context["nb_books"] = BookInstance.objects.filter(user=self.request.user).count()
        context["expenses"] = expenses
        context["messages_nb"] = Message.objects.filter(
            Q(name=self.request.user.username) |
            Q(email=self.request.user.email)
            ).count()
        return context
    
class LoanedBooksListView(PermissionRequiredMixin,LoginRequiredMixin,ListView):
    model = BookInstance
    context_object_name = 'myBooks'
    template_name = 'catalogue/book_instance_list.html'
    permission_required = ('catalog.view_bookinstance')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nb_books"] = BookInstance.objects.all().count()
        prices = 0
        borrowers = []
        for book in BookInstance.objects.all():
            prices+=book.book.price
            if book.user not in borrowers:
                borrowers.append(book.user)
        context["prices"] = prices
        context["nb_messages"] = Message.objects.all().count()
        context["borrower"] = len(borrowers)
        return context

@login_required
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            Activity.objects.create(name=f'Renew the {book_instance.book} to {book_instance.due_back}',user=request.user)
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalogue/book_renew_librarian.html', context)

class AuthorCreateView(CreateView):
    form_class = AuthorForm
    template_name = "catalogue/add_author.html"
    success_url = reverse_lazy("authors")

class AuthorUpdate(UpdateView):
    form_class = AuthorForm
    template_name = "catalog/update_author.html"    
    def get_success_url(self):
        return f'/author/{self.get_object().slug}/'
    def get_queryset(self) :
        queryset = Author.objects.order_by('-id')
        return queryset

class AuthorDelete(DeleteView):
    model = Author
    template_name = "catalog/delete_author.html"
    success_url = reverse_lazy('authors')
    def get_queryset(self) :
        queryset = Author.objects.order_by('-id')
        return queryset
    
# Book

class BookCreateView(CreateView):
    form_class = BookForm
    template_name = "catalogue/forms.html"
    success_url = reverse_lazy('book-create')

class BookUpdate(UpdateView):
    model = Book
    fields = ('title','summary','author','isbn','genre','language')
    template_name = "catalog/update_book.html"    
    def get_success_url(self):
        return f'/book/{self.get_object().slug}/'

class BookDelete(DeleteView):
    model = Book
    template_name = "catalog/delete_book.html"
    success_url = reverse_lazy('books')

class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = "catalogue/blog-detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_object().id == 1:
            for i in range(1,7):
                context[f'blog_{i}'] = self.get_object().blogs.get(id=i)
        elif self.get_object().id == 2 :
            for i in range(6,11):
                context[f'blog_{i-5}'] = self.get_object().blogs.get(id=i)
        # context["first"] = self.get_object().blogs.get(id=1)
        # context["second"] = self.get_object().blogs.get(id=2)
        # context["third"] = self.get_object().blogs.get(id=3)
        # context["forth"] = self.get_object().blogs.get(id=4)
        # context["five"] = self.get_object().blogs.get(id=5)
        return context
    
class BlogCreateView(CreateView):
    model = Blog
    fields = ['title','image','blogs','description']
    template_name = "catalogue/create_blog.html"



def about(request):
    return render(request, 'catalogue/about.html')

#Admin Dash
@login_required
def dashboard(request):
    if request.user.is_staff:
        all_book_instance = BookInstance.objects.all()
        nb_book_instance = all_book_instance.count()
        all_users = User.objects.all()
        new_user = []
        old_user = []
        # print(belha.date_joined.date() + timedelta(weeks=1))
        for user in all_users:
            if user.date_joined.date() + timedelta(weeks=1) < datetime.datetime.now().date():
                old_user.append(user)
            else:
                new_user.append(user)
        users = []
        messages = Message.objects.all()
        for book in all_book_instance:
            if book.user not in users:
                users.append(book.user)
        context = {
            'all_book_instance':nb_book_instance,
            'price' : nb_book_instance * 25,
            'users': len(users),
            'messages_nb':messages.count(),
            'old_users':len(old_user),
            'new_users':len(new_user),
            'book_available':all_book_instance.filter(status='a').count() *50,
            'book_available_percent': math.floor((all_book_instance.filter(status='a').count() / all_book_instance.count() )*100),
            'book_on_loan':all_book_instance.filter(status='o').count() *50,
            'book_on_loan_percent':math.ceil((all_book_instance.filter(status='o').count() / all_book_instance.count() )*100),
            'book_maintenance':all_book_instance.filter(status='m').count() *50,
            'book_maintenance_percent':math.floor((all_book_instance.filter(status='m').count() / all_book_instance.count() )*100),
            'book_reserved':all_book_instance.filter(status='r').count() *50,
            'book_reserved_percent':math.floor((all_book_instance.filter(status='r').count() / all_book_instance.count() )*100),
            'recent_book_instance':all_book_instance[:6],
        }
    else:
        raise PermissionDenied()
    return render(request, 'catalogue/dashboard.html',context)

@login_required
def profile(request):
    form = ProfileForm(instance=Profile.objects.get(user=request.user))
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=Profile.objects.get(user=request.user))
        if form.is_valid():
            print(request.FILES)
            form.save()
            return redirect(reverse_lazy('profile'))
    context = {
        'myMessages':Message.objects.filter(name=request.user.username),
        'messages':Message.objects.all(),
        'form':form,
        'activities':Activity.objects.filter(user=request.user)[:5],
        'activitiesAdmin':Activity.objects.all()[:10],
    }
    return render(request, 'catalogue/profile.html',context)

# def form(request):
#     return render(request, 'catalogue/forms.html')

@login_required
def BookInstanceCreateView(request):
    form = BookInstanceForm()
    if request.method == 'POST':
        form = BookInstanceForm(request.POST or  None)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            Activity.objects.create(name=f'borrow the {Book.objects.get(pk=request.POST.get("book"))}',user=request.user)
            return redirect(reverse_lazy('my-borrowed'))
    context = {
        'form': form
    }
    return render(request,'catalogue/buy_instance.html',context)

# class SignUpView(SuccessMessageMixin, CreateView):
#   form_class = UserRegisterForm
#   template_name = 'registration/register.html'
#   success_url = reverse_lazy('login')
#   success_message = "Your profile was created successfully"
def signUpView(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST.get('username'))
            if user:
                Profile.objects.create(user=user,name=user.username,email=user.email,nikname=user.username)
            return redirect(reverse_lazy('login'))
    context = {
        'form':form
    }
    return render(request,'registration/register.html',context)
        
# class ProfileUpdateView(SuccessMessageMixin,UpdateView):
#     form_class = ProfileForm
#     template_name = "catalogue/profile.html"
#     success_message = "Your profile was updated successfully"
#     success_url = reverse_lazy('profile')
