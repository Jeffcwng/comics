import json
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from xkcd.forms import EmailUserCreationForm
from xkcd.models import Person, Like
from xkcd.utils import get_random_comic
# from django.template import RequestContext
# from comics import settings

@csrf_exempt
def home(request):
    return render(request, "home.html")

@csrf_exempt
def register(request):
        if request.method == 'POST':
            form = EmailUserCreationForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password1']
                form.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect("comics")
        else:
            form = EmailUserCreationForm()
        return render(request, "registration/register.html", {'form': form})


@csrf_exempt
@login_required
def profile(request):
    return render(request, "postlogin/profile.html")

@csrf_exempt
@login_required
def comics(request):
    return render(request, "postlogin/comics.html")

@csrf_exempt
@login_required
def random_search(request):

    user = Person.objects.get(username=request.user.username)
    comic = get_random_comic()
    comic_name = comic['title']
    url = comic['img']

    if request.method == 'POST':
        Like.objects.create(comic_name=comic_name, url=url, like_status=True, liked_by=user)
        response_dict = {'url': '/random_search/'},
        return HttpResponse(json.dumps(response_dict), content_type='application/json')

    else:
        pass

    return render(request, "postlogin/random_search.html", {'comic': comic})

@login_required()
def all_user_likes(request):
    likes = Like.objects.filter(liked_by=request.user)
    print likes

    return render(request, "postlogin/all_user_likes.html", {'likes': likes})