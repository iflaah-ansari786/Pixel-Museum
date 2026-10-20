from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Artwork
import base64
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    return render(request, 'home.html')

def pixel_maker(request):
    return render(request, 'pixel_maker.html')




def gallery(request):
    search_query = request.GET.get('search', '').strip()
    selected_category = request.GET.get('category', '').strip()

    artworks = Artwork.objects.all().order_by('-created_at')

    if search_query:
        artworks = artworks.filter(title__icontains=search_query)

    if selected_category:
        artworks = artworks.filter(category=selected_category)

    context = {
        'artworks': artworks,
        'search_query': search_query,
        'selected_category': selected_category,
    }

    return render(request, 'gallery.html', context)



@require_POST
def save_artwork(request):
    title = request.POST.get('title', '').strip()
    category = request.POST.get('category', 'Nature').strip()
    image_data = request.POST.get('image', '')

    if not title:
        return redirect('pixel_maker')

    if not image_data.startswith('data:image/png;base64,'):
        return redirect('pixel_maker')

    try:
        image_bytes = base64.b64decode(
            image_data.split(',', 1)[1],
            validate=True
        )
    except (ValueError, TypeError):
        return redirect('pixel_maker')

    artwork = Artwork(
        title=title,
        category=category,
        description='Pixel art created using Pixel Museum.',
        owner=request.user if request.user.is_authenticated else None
    )

    artwork.image.save(
        'pixel_art.png',
        ContentFile(image_bytes),
        save=True
    )

    return redirect('gallery')



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            return render(request, 'signup.html', {
                'error': 'Please fill in all fields.'
            })

        if password != confirm_password:
            return render(request, 'signup.html', {
                'error': 'Passwords do not match.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'Username already exists.'
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )
        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')




@login_required
def my_artworks(request):
    artworks = Artwork.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    return render(request, 'my_artworks.html', {
        'artworks': artworks
    })



@login_required
@require_POST
def delete_artwork(request, artwork_id):
    artwork = get_object_or_404(
        Artwork,
        id=artwork_id,
        owner=request.user
    )

    artwork.delete()
    return redirect('my_artworks')



@login_required
def edit_artwork(request, artwork_id):
    artwork = get_object_or_404(
        Artwork,
        id=artwork_id,
        owner=request.user
    )

    if request.method == 'POST':
        artwork.title = request.POST.get('title', '').strip()
        artwork.category = request.POST.get('category', '').strip()
        artwork.description = request.POST.get('description', '').strip()

        if artwork.title and artwork.category:
            artwork.save()
            return redirect('my_artworks')

        error = 'Title and category are required.'
        return render(request, 'edit_artwork.html', {
            'artwork': artwork,
            'error': error
        })

    return render(request, 'edit_artwork.html', {
        'artwork': artwork
    })



@login_required
def user_profile(request):
    artworks = Artwork.objects.filter(owner=request.user)

    context = {
        'username': request.user.username,
        'total_artworks': artworks.count(),
    }

    return render(request, 'profile.html', context)






