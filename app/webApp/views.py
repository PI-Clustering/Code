# Create your views here.
from curses import raw
from math import floor
from operator import mod
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

import csv
from .scripts.driver import get_benchmark
from .models import Benchmark
from .forms import UploadFileForm, ParametersForm
from .scripts.src.main import algorithm_script


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C',
                    '"Testing"', "Here's a quote"])

    return response


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class Index(View):
    template_name = 'webApp/Home.html'

    def get(self, request):
        return render(request, self.template_name, None)

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
        MyVar = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': ['value3', 'value4'],
            'key4': ['value5', 'value6', 'value7', 'value8'],
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


def NeoQuery(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ParametersForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            algo = form.cleaned_data["algo"]
            dataset = form.cleaned_data["dataset"]
            # execute query on Neo...
            # make this async
            results = algorithm_script(dataset, algo)

            # bm = get_benchmark(algo)
            # Benchmark.objects.create(
            # algo_type = bm['algo'], size = bm['size'], run_time = bm['time'])
            # redirect to a new URL:
            return HttpResponseRedirect('/webApp/Benchmark')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ParametersForm()

    return render(request, 'webApp/form_time.html', {'form': form})


# mapping parameters to the url doesn't seem like the correct approach here
def Benchmarks(request):

    bms = Benchmark.objects.all()

    return render(request, "webApp/benchmarks.html", {'bms': bms})
