from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def index(request):
    return render(request, 'core/index.html', {'user': request.user, })
