from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from xkcd.forms import EmailUserCreationForm
# from django.template import RequestContext
# from comics import settings


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
    return render(request, "postlogin/random_search.html")

@csrf_exempt
@login_required
def search_by_date(request):
    return render(request, "postlogin/search_by_date.html")
