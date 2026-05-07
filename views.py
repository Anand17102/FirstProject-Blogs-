from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
@login_required(login_url='/log/')
def create_post(request):
    if request.method=='POST':
        data=request.POST
        image=request.FILES.get("image")
        post_title=data.get('post_title')
        description=data.get('description')

        Blog.objects.create(
            image=image,
            post_title=post_title,
            description=description
        )
        return redirect('/create/')
    print("User:", request.user)
    print("Authenticated:", request.user.is_authenticated)
    return render(request,'temp/create.html')
@login_required(login_url='/log/')
def blog_page(request):
    queryset=Blog.objects.all()
    search=request.GET.get('search')
    if search:
        queryset=queryset.filter(
            Q(post_title__icontains=search)|
            Q(description__icontains=search)
            )
    paginator = Paginator(queryset, 1)  # Show 10 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)
    context={'blogs':page_obj}
    return render(request,'temp/blog.html',context)

@login_required(login_url='/log/')
def delete_blog(request,id):
    blog=Blog.objects.get(id=id)
    blog.delete()
    return redirect('/blogs/')

@login_required(login_url='/log/')
def edit_blog(request,id):
    blog=Blog.objects.get(id=id)
    context={'blogs':blog}
    if request.method=='POST':
        data=request.POST
        image=request.FILES.get("image")
        post_title=data.get('post_title')
        description=data.get('description')

        blog.post_title=post_title
        blog.description=description
        if image:
            blog.image=image
        blog.save()

        return redirect('/blogs/')
    return render(request,'temp/Edit.html',context)

def reg_page(request):
    if request.method=="POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=User.objects.filter(username=username)
        if user.exists():
            messages.error(request,"User already exist")
            return redirect('/reg/')
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request,'Account created successfully')
        return redirect('/reg/')
    return render(request,'temp/reg.html')


def log_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid username')
            return redirect('/log/')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'Invalid password')
            return redirect('/log/')
        else:
            login(request,user)
            return redirect('/blogs/')
    return render(request,'temp/log.html')

def logout_page(request):
    logout(request)
    return redirect('/blogs/')

    
