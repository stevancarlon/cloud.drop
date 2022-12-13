# cloud.drop
#### Video Demo:  https://www.youtube.com/watch?v=R8ETM1qSwP8
#### Description: This was my final project for the **Harvard University's CS50w Course: Web Programming with Python and Javascript**.
#### Live version: https://cloud-drop-app.herokuapp.com/
#

## Distinctiveness and Complexity

>This application developed using Django on the back-end and JavaScript on the front-end allows the user to download videos from YouTube, Instagram and Twitter. The application has a mobile-responsive minimalist design. 

This project is not a social media neither an e-commerce application. 

This webpage is mobile-responsive. None of the projects created during the course had this feature.

This application uses scraping tools. Several scraping tools were considered, the most efficient ones were selected. To download Twitter videos is not as simple as downloading Instagram and YouTube videos and a deep research ended up to be necessary (I wanted to figure out a way to download Twitter videos without using Twitter's API).

This application allows the admin to receive e-mails from a contact form. The design's purpose is to be user-friendly and intuitive.


## Features

- Download videos from Instagram, YouTube and Twitter;
- Toggle menu for mobile users;
- Clear instructions for the user;
- A contact form to report or suggest features.

![This is an image](https://i.ibb.co/ctFyzN3/yt-video-webpage.jpg)

#
## How to use it

To execute the application you must have installed in your system [Python3](https://www.python.org/downloads/) and execute `pip install -r requirements` on the project folder to install the dependencies using a terminal.

![This is an image](https://i.ibb.co/W573HPL/requirements.jpg)

With `Django` already installed, run `python manage.py makemigrations clouddrop`, `python manage.py migrate` and then `python manage.py runserver`.


>**&#x1F53A;IMPORTANT:**

 To use the Instagram video downloader, an account is necessary. Insert the username and password of a instagram account in `def download_instagram(request, url)` on `views.py`.

```python
cl.login('username_here', 'password_here')
```

To download videos, insert a corresponding url into the input text box, click ok and wait for the download button.

![This is an image](https://i.ibb.co/NFg6Tt9/ezgif-5-51043242ba.gif)

This web application was tested on Chrome, Mozila and Opera browsers.

#
## Explaining the back-end code
Some libraries that made this application possible are:
- `pytube` for downloading YouTube videos.
- `instagrapi` for downloading Instagram videos;
- `snscrape` for downloading Twitter videos;

The `download_youtube(request, url):` view is responsible for downloading youtube videos calling the `download_youtube_function(url, filename):` that will use `pytube`. Then the video will be saved into the `youtube_videos` server's folder. The function then will return a `JsonResponse` with the thumbnail url, the title and the video's duration length. The url will receive string treatment on the front-end to extract the post id. If the download is completed succesfully, the user will click the dowload button and trigger the `generate_youtube_link(request, name):` which will download the video to the client.

```python

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

```

On  `download_instagram(request, url):` the function will authenticate a user, download the video using `instagrapi` and call `download_instagram_thumbnail(thumbnail, url):` to download the post's thumbnail. `generate_instagram_link(request, name):` will then generate a download link for the client.

On `download_twitter(request,url):` the function will download the video using `snscrape`. `generate_twitter_link(request, name):` will generate a download link for the client.

On the `contact` view, the function will render the `contact.html` and if the request method is POST, save the data on the Contact table generated by `class Contact(models.Model):` on `models.py`. The admin has the option to receive emails from the form setting the `EMAIL_HOST_USER = 'your_email'` and `EMAIL_HOST_PASSWORD = 'your_password'` variables on `settings.py`.

```python

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('form-name')
        email = request.POST.get('form-email')
        message = request.POST.get('form-message')
        subject = 'CloudDrop e-mail'
        message = f'Name: {name}, e-mail: {email}, message: {message}'

        contact = Contact.objects.create(name=name, email=email, message=message)
        contact.save()

        # IF YOU WANT TO RECEIVE E-MAILS FROM THE CONTACT FORM
        # try:
        #     send_mail(subject, message, settings.EMAIL_HOST_USER, ['cl0ud04ld0@gmail.com'], fail_silently=False) 
        # except BadHeaderError:
        #     return HttpResponse('Invalid header found.')
        # return redirect('index')

    return render(request, 'contact.html')

```

#

## Files information

- `views.py` - Functions to save posts data such as thumbnail, author, title, video, functions to send email messages and functions to generate download links for the client;
- `models.py` - Models to generate a contact table that will register the messages sent by the contact form;
- `urls.py` - Urls paths to call functions and/or render templates;
- `templates` folder - Here lies `layout.html` which contains the nav bar that will be rendered on `index.html` (Youtube), `instagram.html`, `twitter.html` and `contact.html`;
- `static` folder - Contains the css to style the page. Contains JavaScript files such as `download_youtube.js`, `download_instagram.js`,  `download_twitter` to make the back-end to front-end interaction and `toggle.js` to show and hide the menu;
- `download_youtube.js` - Fetch the download youtube view;
- `download_instagram.js` - Fetch the download instagram view;
- `download_twitter.js` - Fetch the download twitter view;
- `settings.py` - Some configurations where made to enable the admin to receive e-mail messages;
- Folders: `youtube_videos`, `instagram_videos` and `twitter_ videos` are the destination of the corresponding downloaded videos. Instagram thumbnails will be saved into `static/ig_thumbs`.

#

## About Harvard University's CS50w Course: Web Programming with Python and Javascript
An course taught by Brian Yu, CS50w  dives deeply into the design and implementation of web apps with Python, JavaScript, and SQL using frameworks like Django, React, and Bootstrap. Topics include database design, scalability, security, and user experience. Through hands-on projects, students learn to write and use APIs, create interactive UIs, and leverage cloud services like GitHub and Heroku. By semester’s end, students emerge with knowledge and experience in principles, languages, and tools that empower them to design and deploy applications on the Internet.

[LinkedIn: Stevan Carlon](https://www.linkedin.com/in/stevancarlon/)
