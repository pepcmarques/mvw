import pandas as pd

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse

from .forms import WalkForm
from .models import Walk


def get_walks(request):
    user = request.user
    walks = Walk.objects.filter(user=user)
    return walks


def walk_chart(request):
    walks = get_walks(request)
    labels, data = walk_bar_chart(walks)

    return JsonResponse(data={
        "labels": labels,
        "data": data,
    })


def walk_bar_chart(walks):
    df = pd.DataFrame.from_records(walks.values())

    labels = [d for d in df["walkDate"]]
    data = [d for d in df["distance"]]

    return labels, data


def home(request):
    walks = get_walks(request)
    total = sum([d.distance for d in walks])
    return render(request, "walk/index.html", {"walks": walks, "walked_distance": total})


def dashboard(request):
    walks = get_walks(request)
    chart_labels, chart_data  = walk_bar_chart(walks)
    return render(request,
                  "walk/dashboard.html",
                  {"walks": walks, "chart_labels": chart_labels, "chart_data": chart_data}
                  )


@login_required()
def add_walk(request):
    if request.method == 'POST':
        form = WalkForm(request.POST)
        if form.is_valid():
            new_walk = form.save(commit=False)
            new_walk.user = request.user
            new_walk.save()
            return redirect(reverse('walk:home'))
    else:
        form = WalkForm()
    return render(request, 'walk/add_walk.html', {'form': form})