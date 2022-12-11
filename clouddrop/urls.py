from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download_youtube/<str:url>', views.download_youtube, name='download_youtube'),
    path('generate_youtube_link/<str:name>', views.generate_youtube_link, name='generate_youtube_link'),
    path('instagram', views.instagram, name='instagram'),
    path('download_instagram/<str:url>', views.download_instagram, name='download_instagram'),
    path('generate_instagram_link/<str:name>', views.generate_instagram_link, name='generate_instagram_link'),
    path('twitter', views.twitter, name='twitter'),
    path('download_twitter/<str:url>', views.download_twitter, name="download_twitter"),
    path('generate_twitter_link/<str:name>', views.generate_twitter_link, name="generate_twitter_link"),
    path('contact', views.contact, name="contact")
]