from django.contrib import admin
from django.urls import path
from webApp.views import Index, Dashboard, Projects, FAQ, About_us, Method2, Method1, RunQuery


app_name = "webApp"
urlpatterns = [
    path('', Index.as_view(), name='Home'),
    path('Dashboard/', Dashboard.as_view(), name='Dashboard'),
    path('Projects/', Projects.as_view(), name='Projects'),
    path('FAQ/', FAQ.as_view(), name='FAQ'),
    path('About_us/', About_us.as_view(), name='About_us'),
    path('Method1/', Method1.as_view(), name='Method1'),
    path('Method2/', Method2.as_view(), name='Method2'),
    path('RunQuery/', RunQuery.as_view(), name="RunQuery")
]
