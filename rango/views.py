from datetime import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .forms import *
from .models import Category, Page

def index(request):
    
    context_dict = {}
    context_dict['categories'] = Category.objects.order_by('-likes')[:5]
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['pages'] = Page.objects.order_by('-views')[:5]
    
    response =  render(request,'rango/index.html', context = context_dict, visits=request.COOKIES.get('visits',1))
    visitor_cookie_handler(request,response)
    return response
    

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

@login_required
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
    
    
@login_required  
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
    
    
    
def register(request):
    registered = False
    
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user # links the 2 models together
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)
    
    # GET        
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
        
    # GET or POST
    return render(request, 'rango/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})
    
    
    

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    # GET
    else:
        return render(request, 'rango/login.html')
    
    
    
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))



def visitor_cookie_handler(request, response):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        response.set_cookie('last_visit', last_visit_cookie)
        
    response.set_cookie('visits', visits)
        
    