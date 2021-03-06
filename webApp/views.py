# Create your views here.
from curses import raw
from math import floor, exp
from operator import mod
import random
from typing import Any, Dict, List, Tuple
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django import forms
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, FileResponse

import csv
from .models import Benchmark, DataPoint
from .forms import UploadFileForm, ParametersForm, NodesForm
from .scripts.src.main import algorithm_script
from .scripts.src.incremental_scheme import run_add_node
from .scripts.db import get_data


class BenchmarkListView(ListView):
    model = Benchmark


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


def node_csv(request):
    response = FileResponse(open("webApp/scripts/graph/node.csv", "rb"))
    return response


def edge_csv(request):
    response = FileResponse(open("webApp/scripts/graph/edge.csv", "rb"))
    return response


def bench_jpg(request):
    response = FileResponse(open("webApp/scripts/graph/bench.jpg", "rb"))
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


def AddDummyData():
    for _ in range(50):
        Benchmark.objects.create(
            algo_type=random.choice(
                ["K-Means", "Mean Shift", "DBSCAN"]),
            size=50,
            t_pre=random.uniform(0, 10),
            t_cluster=random.uniform(10, 50),
            t_write=random.uniform(10, 12)
        )


def AddNode(request):
    if request.method == 'POST':
        form = NodesForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Do something
            # run_function(data)
            run_add_node(data)
            # redirect to a new URL:
            return HttpResponseRedirect('/Results')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NodesForm()

    return render(request, 'webApp/form_nodes.html', {'form': form})


def RunAlgo(request):
    if request.method == 'POST':
        form = ParametersForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # execute query on Neo...
            # make this async
            results = algorithm_script(data)
            # redirect to a new URL:
            return HttpResponseRedirect('/Results')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ParametersForm()

    return render(request, 'webApp/form_time.html', {'form': form})


def Dashboard(request):

    return render(request, "webApp/dashboard.html")


def get_chart_data(request):

    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html

    data = get_data()

    return JsonResponse(data)


def Results(request):

    bms = Benchmark.objects.all()[:20]

    return render(request, "webApp/results.html", {'bms': bms})
