
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pixel-maker/', views.pixel_maker, name='pixel_maker'),
    path('gallery/', views.gallery, name='gallery'),
    path('save-artwork/', views.save_artwork, name='save_artwork'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('my-artworks/', views.my_artworks, name='my_artworks'),
    path('my-artworks/delete/<int:artwork_id>/', views.delete_artwork, name='delete_artwork'),
    path('my-artworks/edit/<int:artwork_id>/', views.edit_artwork, name='edit_artwork'),
    path('profile/', views.user_profile, name='user_profile'),



]
