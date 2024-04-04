"""
    Docstring describing your form class.

    You can provide details about the purpose of the form, what fields it contains,
    and any special behavior or usage instructions.
"""
from datetime import datetime, timedelta  # Standard library imports
from django.db import models  # Third-party import
from django.contrib.auth.models import User  # Third-party import


class StudentExtra(models.Model):
    """
    Docstring describing your form class.

    You can provide details about the purpose of the form, what fields it contains,
    and any special behavior or usage instructions.
"""
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)
    #used in issue book
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']' # pylint: disable=no-member
    @property
    def get_name(self): # pylint: disable=missing-function-docstring
        return self.user.first_name # pylint: disable=no-member
    @property
    def getuserid(self): # pylint: disable=missing-function-docstring
        return self.user.id # pylint: disable=no-member


class Book(models.Model):
    """
    Docstring describing your form class.

    You can provide details about the purpose of the form, what fields it contains,
    and any special behavior or usage instructions.
"""
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('novel', 'Novel'),
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('scifi','Sci-Fi')
        ]
    name=models.CharField(max_length=30)
    isbn=models.PositiveIntegerField()
    author=models.CharField(max_length=40)
    category=models.CharField(max_length=30,choices=catchoice,default='education')
    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'


def get_expiry(): # pylint: disable=missing-function-docstring
    return datetime.today() + timedelta(days=15)
class IssuedBook(models.Model): # pylint: disable=missing-class-docstring
    #moved this in forms.py
    enrollment=models.CharField(max_length=30)
    #isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    def __str__(self): # pylint: disable=missing-class-docstring
        return str(self.enrollment)
    