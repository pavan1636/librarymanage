"""
    Docstring describing your form class.

    You can provide details about the purpose of the form, what fields it contains,
    and any special behavior or usage instructions.
"""
from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    '''
    hhh
    '''
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))




class AdminSigupForm(forms.ModelForm):
    '''
    hhh
    '''
    def some_method(self):
        '''
        Public method description.
        '''
    class Meta: # pylint: disable=too-few-public-methods
        '''
        hhh
        '''
        model=User
        fields=['first_name','last_name','username','password']



class StudentUserForm(forms.ModelForm):
    '''
    hhh
    '''
    def some_method(self):
        '''
        Public method description.
        '''
    class Meta:# pylint: disable=too-few-public-methods
        '''
    hhh
    '''
        model=User
        fields=['first_name','last_name','username','password']

class StudentExtraForm(forms.ModelForm):
    '''
    hhh
    '''
    def some_method(self):
        '''
        Public method description.
        '''
    class Meta:# pylint: disable=too-few-public-methods
        '''
    hhh
    '''
        model=models.StudentExtra
        fields=['enrollment','branch']

class BookForm(forms.ModelForm):
    '''
    hhh
    '''
    def some_method(self):
        '''
        Public method description.
        '''
    class Meta:# pylint: disable=too-few-public-methods
        '''
    hhh
    '''
        model=models.Book
        fields=['name','isbn','author','category']
class IssuedBookForm(forms.Form):
    '''
    hhh
    '''
    def some_method(self):
        '''
        Public method description.
        '''
    #to_field_name value will be stored when form is submitted.....
    isbn2 = forms.ModelChoiceField(
    # pylint: disable=no-member
    queryset=models.Book.objects.all(),
    # pylint: enable=no-member
    empty_label="Name and ISBN",
    to_field_name="isbn",
    label='Name and ISBN'
)
    enrollment2 = forms.ModelChoiceField(
    # pylint: disable=no-member
    queryset=models.StudentExtra.objects.all(),
    # pylint: enable=no-member
    empty_label="Name and Enrollment",
    to_field_name='enrollment',
    label='Name and Enrollment'
)
    