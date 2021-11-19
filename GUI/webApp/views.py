from django.shortcuts import render

# Create your views here.

# Create your views here.
from django.http import HttpResponse
from django.views import View
from .models import Book


class Index(View):
    template_name = 'webApp/Home.html'

    def get(self, request):
        books = Book.objects.filter(Name='fatemeh')
        #book1 = Book.objects.get(Name='asghar2')
        # print(books)
        #print(books[0].id)
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
            'khar': '',
            'arman': 'khar ast',
            'hhhh': ['keyk','chai'],
            'navbar': ['Arman', 'Fatemeh', 'Rasoul', 'cake', 'latte'],
            'books': Book.objects.all(),

        }
        return render(request, self.template_name, MyVar)

#----------------------Dashboard----------------------------#


class Dashboard(View):
    template_name = 'webApp/Dashboard.html'

    def get(self, request):
        MyVar = {
            'khar': '',
            'arman': 'khar ast',
            'hhhh': ['keyk','chai'],
            'navbar' : ['Arman', 'Fatemeh', 'Rasoul', 'cake', 'latte'],

        }
        return render(request, self.template_name, MyVar)


#-----------------------FAQ----------------------------#


class FAQ(View):
    template_name = 'webApp/FAQ.html'

    def get(self, request):
        MyVar = {
            'khar': '',
            'arman': 'khar ast',
            'hhhh': ['keyk','chai'],
            'navbar' : ['Arman', 'Fatemeh', 'Rasoul', 'cake', 'latte'],

        }
        return render(request, self.template_name, MyVar)

#---------------------About us-------------------------#



class About_us(View):
    template_name = 'webApp/About_us.html'

    def get(self, request):
        MyVar = {
            'khar': '',
            'arman': 'khar ast',
            'hhhh': ['keyk','chai'],
            'navbar' : ['Arman', 'Fatemeh', 'Rasoul', 'cake', 'latte'],

        }
        return render(request, self.template_name, MyVar)

#-----------------------------Projects--------------------------#


class Projects(View):
    template_name = 'webApp/Projects.html'

    def get(self, request):
        MyVar = {
            'khar': '',
            'arman': 'khar ast',
            'hhhh': ['keyk','chai'],
            'navbar' : ['Arman', 'Fatemeh', 'Rasoul', 'cake', 'latte'],

        }
        return render(request, self.template_name, MyVar)

class Method1(View):
    template_name = 'webApp/Method1.html'

    def get(self, request):
        MyVar = {
            'khar': '',
            'arman': 'khar ast',
            'hhhh': ['keyk','chai'],
            'navbar' : ['Arman', 'Fatemeh', 'Rasoul', 'cake', 'latte'],

        }
        return render(request, self.template_name, MyVar)
class Method2(View):
    template_name = 'webApp/Method2.html'

    def get(self, request):
        MyVar = {
            'khar': '',
            'arman': 'khar ast',
            'hhhh': ['keyk','chai'],
            'navbar' : ['Arman', 'Fatemeh', 'Rasoul', 'cake', 'latte'],

        }
        return render(request, self.template_name, MyVar)