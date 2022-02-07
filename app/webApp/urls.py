from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # add this
from django.conf.urls.static import static  # add this
# Index, Dashboard, Projects, FAQ, About_us, Method2, Method1, RunQuery
from . import views

app_name = "webApp"
urlpatterns = [
    path('', views.Index.as_view(), name='Home'),
    path('Dashboard/', views.Dashboard.as_view(), name='Dashboard'),
    path('Projects/', views.Projects.as_view(), name='Projects'),
    path('FAQ/', views.FAQ.as_view(), name='FAQ'),
    path('About_us/', views.About_us.as_view(), name='About_us'),
    path('Method1/', views.Method1.as_view(), name='Method1'),
    path('Method2/', views.Method2.as_view(), name='Method2'),
    path('RunQuery/', views.NeoQuery, name='RunQuery'),
    path('Benchmark/', views.Benchmarks),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)