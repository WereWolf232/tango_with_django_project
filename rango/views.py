from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse

from .forms import CategoryForm,PageForm
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


def add_category(request):
    form = CategoryForm()
    
    if request.method =="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            # commit=True by default
            form.save()

            return redirect(reverse("rango:index"))
            
        else:
            print(form.errors)
            
    return render(request, 'rango/add_category.html', {'form': form})
    
    
    
def add_page(request, category_name_slug):
    form = PageForm()
    
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    if category is None:
        return redirect(reverse("rango:index"))
    
    if request.method =="POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            
        else:
            print(form.errors)
            return redirect(reverse("rango:index"))
            
    # Get
    else:
        return render(request, 'rango/add_page.html', {'form': form, 'category': category})