# Create your views here.
from curses import raw
from math import floor
from django.http import HttpResponse
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django import forms
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .forms  import DocumentForm
import csv
#from .scripts.driver import get_benchmark
from .models import Book, Benchmark
from .forms import UploadFileForm, TimerForm


# def some_view(request):
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(
#         content_type='text/csv',
#         headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
#     )
#
#     writer = csv.writer(response)
#     writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
#     writer.writerow(['Second row', 'A', 'B', 'C',
#                     '"Testing"', "Here's a quote"])
#
#     return response


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class Index(View):
    template_name = 'webApp/Home.html'

    def get(self, request):
        books = Book.objects.filter(Name='fatemeh')
        # book1 = Book.objects.get(Name='asghar2')
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
            'key4': ['value5', 'value6', 'value7', 'value8'],

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
            'key4': ['value5', 'value6', 'value7', 'value8'],

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
            'key4': ['value5', 'value6', 'value7', 'value8'],

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
            'key4': ['value5', 'value6', 'value7', 'value8'],

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
            'key4': ['value5', 'value6', 'value7', 'value8'],

        }
        return render(request, self.template_name, MyVar)


class Method1(View):
    template_name = 'webApp/Method1.html'

    def get(self, request):
        MyVar = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': ['value3', 'value4'],
            'key4': ['value5', 'value6', 'value7', 'value8'],

        }
        return render(request, self.template_name, MyVar)


class Method2(View):
    template_name = 'webApp/Method2.html'
    def get(self, request):
        server_form = DocumentForm()
        MyVar = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': ['value3', 'value4'],
            'key4': ['value5', 'value6', 'value7', 'value8'],
        }
        return render(request, self.template_name, {'server_form': server_form, 'MyVar': MyVar})


        # return render(request, self.template_name, MyVar)

    # def simple_upload(self, request):
    #     if request.method == 'POST' and request.FILES['myfile']:
    #         myfile = request.FILES['myfile']
    #         fs = FileSystemStorage()
    #         filename = fs.save(myfile.name, myfile)
    #         uploaded_file_url = fs.url(filename)
    #         return render(request, self.template_name, {
    #             'uploaded_file_url': uploaded_file_url
    #         })
    #     return render(request, self.template_name)
    def post(self, request):
        if request.method == 'POST':
            print("hi")
            form = DocumentForm(request.POST, request.FILES)
            print(form["document"])
            if form.is_valid():
                print('hi2')
                form.save()
                return redirect("webApp:Method1")
        else:
            form = DocumentForm()
        return render(request, self.template_name, {
        'form': form
    })



def NeoQuery(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TimerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            dataset = form.cleaned_data["dataset"]
            algo = form.cleaned_data["algo"][0]
            # execute query on Neo...
            # this now gets data back from neo - start here
            bm = get_benchmark(dataset, algo, None)

            Benchmark.objects.create(
                algo_type=bm['algo'], size=bm['size'], run_time=bm['time'])
            # redirect to a new URL:
            return HttpResponseRedirect('/webApp/Benchmark')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TimerForm()

    return render(request, 'webApp/form_time.html', {'form': form})


# mapping parameters to the url doesn't seem like the correct approach here
def Benchmarks(request):

    bms = Benchmark.objects.all()

    return render(request, "webApp/benchmarks.html", {'bms': bms})
