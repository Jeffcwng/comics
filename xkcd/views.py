from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# from django.template import RequestContext
# from comics import settings


def home(request):
    return render(request, "prelogin/index.html")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserCreationForm()

    return render(request, "prelogin/register.html", {
        'form': form,
    })


@csrf_exempt
@login_required
def profile(request):
    if not request.user.is_authenticated():
        return redirect("prelogin/login")
    return render(request, "postlogin/profile.html")
