# from django.contrib import admin
# from .models import Book,StudentExtra,IssuedBook
# # Register your models here.
# class BookAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Book, BookAdmin)


# class StudentExtraAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(StudentExtra, StudentExtraAdmin)


# class IssuedBookAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(IssuedBook, IssuedBookAdmin)

"""
Module for registering models with the Django admin site.
"""

from django.contrib import admin
from .models import Book, StudentExtra, IssuedBook

class BookAdmin(admin.ModelAdmin):
    """
    Admin class for customizing the Book model in the Django admin interface.
    """

admin.site.register(Book, BookAdmin)


class StudentExtraAdmin(admin.ModelAdmin):
    """
    Admin class for customizing the StudentExtra model in the Django admin interface.
    """

admin.site.register(StudentExtra, StudentExtraAdmin)


class IssuedBookAdmin(admin.ModelAdmin):
    """
    Admin class for customizing the IssuedBook model in the Django admin interface.
    """

admin.site.register(IssuedBook, IssuedBookAdmin)
