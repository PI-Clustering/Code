from django.contrib import admin
from .models import Book, Document

admin.site.register(Book)
# Register your models here.
admin.site.register(Document)