from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # add this
from django.conf.urls.static import static  # add this
from django.views.generic.base import TemplateView
# Index, Dashboard, Projects, FAQ, About_us, Method2, Method1, RunQuery
from . import views

app_name = "webApp"
urlpatterns = [
    path('', views.RunAlgo, name='Home'),
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('Benchmarks/', views.BenchmarkListView.as_view(), name='Benchmarks'),
    path('Results/', views.Results, name='Results'),
    path('AddNode/', views.AddNode, name='AddNode'),
    path('GetChartData/', views.get_chart_data),
    path('Submit/', views.RunAlgo, name='Submit'),
    path('Projects/', views.Projects.as_view(), name='Projects'),
    path('About_us/', views.About_us.as_view(), name='About_us'),
    path('Method1/', views.Method1.as_view(), name='Method1'),
    path('Method2/', views.Method2.as_view(), name='Method2'),
    path('node.csv', views.node_csv),
    path('edge.csv', views.edge_csv),
    path('bench.jpg', views.bench_jpg)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
