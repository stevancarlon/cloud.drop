from django.shortcuts import render
from pytube import YouTube
from django.views.decorators.csrf import csrf_exempt
import os, mimetypes
from django.shortcuts import redirect
import datetime
from django.http import HttpResponse, JsonResponse, FileResponse
from instagrapi import Client
import snscrape.modules.twitter as sntwitter
import urllib.request
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .models import Contact

# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def download_youtube(request, url):
    filename = url
    url = 'https://www.youtube.com/watch?v=' + url
    print(url)
    print('Starting download...')
    download_youtube_function(url, filename)

    current_path = os.path.dirname(os.path.abspath(__file__))
    output_path = current_path + '/youtube_videos/' + filename + '.mp4'

    thumbnail = YouTube(url)
    title = thumbnail.title
    length = str(datetime.timedelta(seconds=thumbnail.length))
    thumbnail = thumbnail.thumbnail_url

    return JsonResponse({"filepath": output_path, "thumbnail": thumbnail, "title": title, "length": length}, status=400)

@csrf_exempt
def download_youtube_function(url, filename):
    youtubeObject = YouTube(url)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    youtubeObject_2 = YouTube(url)
    youtubeObject_2 = youtubeObject_2.streams.get_by_resolution(resolution='360p')
    current_path = os.path.dirname(os.path.abspath(__file__))

    output_path = current_path + '/youtube_videos/'
    try:
        print('Running pytube...')
        youtubeObject_2.download(output_path=output_path, filename=filename + '_res_360p.mp4')
        youtubeObject.download(output_path=output_path, filename=filename + '_res_720p.mp4')
    except:
        print("An error has occurred")
    print("Download is completed successfully")
    # return JsonResponse({'Debug':'test'}, safe=False)

@csrf_exempt
def generate_youtube_link(request, name):
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = current_path + '/youtube_videos/' + name + '.mp4'

    f = open(file_path, 'rb')
    mime_type, _ = mimetypes.guess_type(file_path)
    print(mime_type)
    
    response = FileResponse(f, content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename={name}.mp4'

    return response

def instagram(request):
    return render(request, 'instagram.html')

@csrf_exempt
def download_instagram(request, url):
    print('download instagram debug')
    print('Starting download...')

    complete_url = "https://www.instagram.com/p/" + url
    current_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_path + '/instagram_videos/')

    cl = Client()
    cl.login('username_here', 'password_here')

    pk = cl.media_pk_from_url(complete_url)
    d = cl.media_info(pk).dict()

    video_url = d['video_url']

    urllib.request.urlretrieve(video_url, url + '.mp4')

    username = d['user']['username']
    text = d['caption_text'][0:60] 
    thumbnail = d['thumbnail_url']  

    download_instagram_thumbnail(thumbnail, url)

    return JsonResponse({'author': username, 'title': text, 'thumbnail': thumbnail}, status=400) 
    

@csrf_exempt
def download_instagram_thumbnail(thumbnail, url):
    current_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_path + '/static/ig_thumbs/')
    urllib.request.urlretrieve(thumbnail, url + '.jpg')

def generate_instagram_link(request, name):
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = current_path + '/instagram_videos/' + name + '.mp4'

    f = open(file_path, 'rb')
    mime_type, _ = mimetypes.guess_type(file_path)
    print(mime_type)
    
    response = FileResponse(f, content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename={name}.mp4'

    return response

def twitter(request):
    return render(request, 'twitter.html')

@csrf_exempt
def download_twitter(request, url):
    url_id = url
    url = 'https://twitter.com/BornAKang/status/' + url
    current_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_path + '/twitter_videos/')

    tweet_author = url.rsplit('https://twitter.com/', 1)[1]
    tweet_author = tweet_author.rsplit('/status/', 1)[0]

    query = f"(from:{tweet_author})"

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():

        if tweet.url == url:
            tweet_dict = vars(tweet)

            video_url = str(tweet_dict['media'][0])
            video_url = video_url.rsplit("variants=[VideoVariant(contentType='video/mp4', url='")[1]
            video_url = video_url.rsplit("', bitrate=950000)")[0]
            urllib.request.urlretrieve(video_url, url_id + '.mp4') 

            thumbnail_url = str(tweet_dict['media'][0])
            thumbnail_url = thumbnail_url.rsplit("Video(thumbnailUrl='")[1]
            thumbnail_url = thumbnail_url.rsplit("', variants=[VideoVariant(contentType='")[0]
            print(thumbnail_url)

            tweet_text = tweet_dict['content']
            break
    print('debug')
    return JsonResponse({'thumbnail':thumbnail_url, 'tweet_text': tweet_text[0:60], 'video_url': video_url, 'author': tweet_author}, status=400)

@csrf_exempt
def generate_twitter_link(request, name):
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = current_path + '/twitter_videos/' + name + '.mp4'

    f = open(file_path, 'rb')
    mime_type, _ = mimetypes.guess_type(file_path)
    print(mime_type)
    
    response = FileResponse(f, content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename={name}.mp4'

    return response

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('form-name')
        email = request.POST.get('form-email')
        message = request.POST.get('form-message')
        subject = 'CloudDrop e-mail'
        message = f'Name: {name}, e-mail: {email}, message: {message}'

        contact = Contact.objects.create(name=name, email=email, message=message)
        contact.save()

        #IF YOU WANT TO RECEIVE E-MAILS FROM THE CONTACT FORM
        # try:
        #     send_mail(subject, message, settings.EMAIL_HOST_USER, ['cl0ud04ld0@gmail.com'], fail_silently=False) 
        # except BadHeaderError:
        #     return HttpResponse('Invalid header found.')
        # return redirect('index')

    return render(request, 'contact.html')
    
