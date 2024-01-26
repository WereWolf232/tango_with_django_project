from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Page

def index(request):
    context_dict = {}
    context_dict['categories'] = Category.objects.order_by('-likes')[:5]
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['pages'] = Page.objects.order_by('-views')[:5]
    return render(request,'rango/index.html', context = context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict = {"category": category, "pages": pages}
        
        
    except:
        context_dict = {"category": None, "pages": None}
        
    print(context_dict.values())
    return render(request, 'rango/category.html', context=context_dict)