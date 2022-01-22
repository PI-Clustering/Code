from django.shortcuts import render

# Create your views here.

# Create your views here.
from django.http import HttpResponse
from django.views import View
from .models import Book
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django import forms
# from .models import Document
# from .forms import DocumentForm
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
class Index(View):
    template_name = 'webApp/Home.html'

    def get(self, request):
        books = Book.objects.filter(Name='fatemeh')
        #book1 = Book.objects.get(Name='asghar2')
        # print(books)
        # print(books[0].id)
        # mybook = books[0]
        # mybook.Name = 'kobra'
        # mybook.save()
        # print(mybook)
        # books[0].Name = 'fatemeh' it doesn't fucking work!!!!
        # books[0].save()
        # for i in books:
        #     i.Name = 'fatemeh'
        #     i.save()
        # print(Book.objects.get(id=Book.objects.filter(Name='sara')[0].id))
        # book2 = Book.objects.get(id=Book.objects.filter(Name='sara')[0].id)
        # # book2.Name='sara'
        # # book2.save()
        # book2.delete()
        # book3 = Book(Name='arman', ISBN=987)
        # print(book3.id)
        # # book3.save()
        # id1 = Book.objects.create(Name='dfghj',ISBN=5678).id
        # print(id1)
        # motoghayer = Book.objects.get_or_create(Name='khar')
        # print(motoghayer)

        MyVar = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': ['value3', 'value4'],
            'key4' : ['value5', 'value6', 'value7', 'value8'],

        }
        return render(request, self.template_name, MyVar)

#----------------------Dashboard----------------------------#


class Dashboard(View):
    template_name = 'webApp/Dashboard.html'

    def get(self, request):
        MyVar = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': ['value3', 'value4'],
            'key4' : ['value5', 'value6', 'value7', 'value8'],

        }
        return render(request, self.template_name, MyVar)


#-----------------------FAQ----------------------------#


class FAQ(View):
    template_name = 'webApp/FAQ.html'

    def get(self, request):
        MyVar = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': ['value3', 'value4'],
            'key4' : ['value5', 'value6', 'value7', 'value8'],

        }
        return render(request, self.template_name, MyVar)

#---------------------About us-------------------------#


class About_us(View):
    template_name = 'webApp/About_us.html'

    def get(self, request):
        MyVar = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': ['value3', 'value4'],
            'key4' : ['value5', 'value6', 'value7', 'value8'],

        }
        return render(request, self.template_name, MyVar)

#-----------------------------Projects--------------------------#


class Projects(View):
    template_name = 'webApp/Projects.html'

    def get(self, request):
        MyVar = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': ['value3', 'value4'],
            'key4' : ['value5', 'value6', 'value7', 'value8'],

        }
        return render(request, self.template_name, MyVar)


class Method1(View):
    template_name = 'webApp/Method1.html'

    def get(self, request):
        MyVar = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': ['value3', 'value4'],
            'key4' : ['value5', 'value6', 'value7', 'value8'],

        }
        return render(request, self.template_name, MyVar)


class Method2(View):
    template_name = 'webApp/Method2.html'

    def get(self, request):
        MyVar = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': ['value3', 'value4'],
            'key4' : ['value5', 'value6', 'value7', 'value8'],

class RunQuery(View):
    template_name = 'webApp/RunQuery.html'

    def get(self, request):
        data = {
        }
        return render(request, self.template_name, MyVar)
    def simple_upload(self, request):
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return render(request, self.template_name, {
            'uploaded_file_url': uploaded_file_url
        })
        return render(request, self.template_name)