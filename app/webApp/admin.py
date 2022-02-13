from django.contrib import admin
from .models import Document, Benchmark

# Register your models here.
admin.site.register(Benchmark)
admin.site.register(Document)
