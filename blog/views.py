from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import BlogPost
from .forms import BlogPostForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

@login_required
def create_or_edit_post(request, pk=None):
    post = None
    is_edit = False
    if pk:
        post = BlogPost.objects.get(pk=pk)
        is_edit = True
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)

            if 'image' in request.FILES:
                image = request.FILES['image']
                img = Image.open(image)

                img_format = 'JPEG' if img.format not in ['PNG'] else 'PNG'
                content_type = 'image/jpeg' if img_format == 'JPEG' else 'image/png'

                # Resize if width > 800
                max_width = 800
                if img.width > max_width:
                    height = int((max_width / float(img.width)) * float(img.height))
                    img = img.resize((max_width, height), Image.ANTIALIAS)

                # Save to memory
                img_io = io.BytesIO()
                img.save(img_io, format=img_format, quality=85)
                img_io.seek(0)

                # Replace image with compressed version
                instance.image = InMemoryUploadedFile(
                    img_io, None, image.name, content_type, img_io.tell(), None
                )

            instance.save()
            return redirect('dashboard')
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/create_or_edit_post.html', {'form': form, 'is_edit': is_edit})

def create_or_edit_post(request, pk=None):
    post = None
    is_edit = False
    if pk:
        post = Post.objects.get(pk=pk)
        is_edit = True
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # Handle image compression before saving
            instance = form.save(commit=False)
            
            if 'image' in request.FILES:
                image = request.FILES['image']
                img = Image.open(image)
                img_format = img.format

                # Resize the image if it's too large
                max_width = 800
                if img.width > max_width:
                    height = int((max_width / float(img.width)) * float(img.height))
                    img = img.resize((max_width, height), Image.ANTIALIAS)

                # Compress the image (reduce quality to 85%)
                img_io = io.BytesIO()
                img.save(img_io, format=img_format, quality=85)
                img_io.seek(0)

                # Create a new InMemoryUploadedFile and assign it to the instance
                instance.image = InMemoryUploadedFile(
                    img_io, None, image.name, 'image/jpeg', img_io.tell(), None
                )
            
            instance.save()
            return redirect('dashboard')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/create_or_edit_post.html', {'form': form, 'is_edit': is_edit})


def dashboard(request):
    posts_list = BlogPost.objects.all().order_by('-created_at')  # Get all blog posts, ordered by creation date
    paginator = Paginator(posts_list, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')  # Get the current page number from the query string
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page
    return render(request, 'blog/dashboard.html', {'page_obj': page_obj})



@login_required
def list_posts(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/list_posts.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_posts')
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'is_edit': False})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('list_posts')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'is_edit': True})

def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('list_posts')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # start session
            return redirect(request.GET.get('next', 'list_posts'))  # redirect to the original page or the list of posts
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'blog/login.html')

@login_required
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('dashboard') 
    

def list_posts(request):  # This will be your homepage/dashboard
    posts = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/dashboard.html', {'page_obj': page_obj})

def all_posts(request):  # This will be used for View All Posts
    posts = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/list_posts.html', {'page_obj': page_obj})




