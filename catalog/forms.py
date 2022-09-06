from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from .models import Author,Book,BookInstance,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ("name","email","nikname","image","website","skills")
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).",widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
            raise ValidationError(_("the new date in the future not in the past you idiot!"))
        if data > (datetime.date.today() + datetime.timedelta(weeks=4)):
            raise ValidationError(_("you will borrow the book not owned ! pick it for a short time"))
        return data

class AuthorForm(forms.ModelForm):
    
    class Meta:
        model = Author
        fields = ['name', 'date_birth', 'date_death']
        widgets = {
            'date_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_death': forms.DateInput(attrs={'type': 'date'})
        }
    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # if visible.field.widget.input_type == 'text':
            #     print(visible.field)
            visible.field.widget.attrs['class'] = 'form-control form-control-rounded'

class BookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ['title','author','summary','image','language','genre','isbn']
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class BookInstanceForm(forms.ModelForm):
    
    class Meta:
        model = BookInstance
        fields = ("book","due_back","imprint","status")
        widgets = {
            'due_back': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(BookInstanceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
   
    def clean_due_back(self):
        due_back = self.cleaned_data.get('due_back')
        if due_back < datetime.date.today():
            raise ValidationError("Please Enter A valid Date ")
        return due_back 