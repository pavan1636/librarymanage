"""
    Docstring describing your form class.

    You can provide details about the purpose of the form, what fields it contains,
    and any special behavior or usage instructions.
"""
# pylint: disable=ungrouped-imports,unused-import
# pylint: disable=wrong-import-order
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from datetime import datetime, timedelta, date

from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from librarymanage.settings import EMAIL_HOST_USER
from . import forms, models
from .models import Book
from .forms import BookForm




def home_view(request):# pylint: disable=missing-function-docstring
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

#for showing signup/login button for student
def studentclick_view(request): # pylint: disable=missing-function-docstring
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for teacher
def adminclick_view(request): # pylint: disable=missing-function-docstring
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')



def adminsignup_view(request):# pylint: disable=missing-function-docstring
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})






def studentsignup_view(request):# pylint: disable=missing-function-docstring
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            # pylint: disable=unused-variable
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)




def is_admin(user):# pylint: disable=missing-function-docstring
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):# pylint: disable=missing-function-docstring
    # pylint: disable=no-else-return
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):# pylint: disable=missing-function-docstring
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            # pylint: disable=unused-variable
            user=form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)# pylint: disable=no-member
def viewbook_view(request):# pylint: disable=missing-function-docstring
    books=models.Book.objects.all()# pylint: disable=no-member
    return render(request,'library/viewbook.html',{'books':books})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):# pylint: disable=missing-function-docstring
    form=forms.IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'library/bookissued.html')
    return render(request,'library/issuebook.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin) # pylint: disable=no-member
def viewissuedbook_view(request):# pylint: disable=missing-function-docstring
    issuedbooks=models.IssuedBook.objects.all()# pylint: disable=no-member
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=date.today()-ib.issuedate
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))# pylint: disable=no-member
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))# pylint: disable=no-member
        i=0
        # pylint: disable=unused-variable
        for l in books:
            t = (
    students[i].get_name,
    students[i].enrollment,
    books[i].name,
    books[i].author,
    issdate,
    expdate,
    fine
)

            i=i+1
            li.append(t)

    return render(request,'library/viewissuedbook.html',{'li':li})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):# pylint: disable=missing-function-docstring
    students=models.StudentExtra.objects.all()# pylint: disable=no-member
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):# pylint: disable=missing-function-docstring
    student=models.StudentExtra.objects.filter(user_id=request.user.id)# pylint: disable=no-member
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)# pylint: disable=no-member

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)# pylint: disable=no-member
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=date.today()-ib.issuedate
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})

def aboutus_view(request):# pylint: disable=missing-function-docstring
    return render(request,'library/aboutus.html')

def contactus_view(request):# pylint: disable=missing-function-docstring
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(
    str(name) + ' || ' + str(email),
    message,
    EMAIL_HOST_USER,
    ['wapka1503@gmail.com'],
    fail_silently=False
)

            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form':sub})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def edit_book(request, book_id):# pylint: disable=missing-function-docstring
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return render(request, 'library/viewbook.html', {'books': Book.objects.all()})# pylint: disable=no-member
    else:
        form = BookForm(instance=book)
    return render(request, 'library/editbook.html', {'form': form, 'book': book})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_book(request, book_id):# pylint: disable=missing-function-docstring
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    books = Book.objects.all()# pylint: disable=no-member
    return render(request, 'library/viewbook.html', {'books': books})
