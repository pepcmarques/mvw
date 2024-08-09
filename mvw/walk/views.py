import pandas as pd

from django.contrib.auth.decorators import login_required
from django.db.models import Func, Sum
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse

from .forms import WalkForm
from .models import Walk, VisitingPoint


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

    if df.shape == (0, 0):
        return None, None

    labels = [d for d in df["walkDate"]]
    data = [d for d in df["distance"]]

    return labels, data


def get_goal_and_points():
    # points = VisitingPoint.objects.all().order_by('order_no').values()
    points = (
        VisitingPoint.objects.annotate(
            cumsum=Func(
                Sum('km'),
                template='%(expressions)s OVER (ORDER BY %(order_by)s)',
                order_by="id"
            )
        ).values('order_no', 'picture_name', 'name', 'km', 'description', 'cumsum').order_by('order_no', 'cumsum')
    )
    print(points)
    goal = sum([p["km"] for p in points])
    return goal, points


@login_required()
def home(request):
    walks = get_walks(request)
    goal_km, points = get_goal_and_points()
    total = sum([d.distance for d in walks])
    return render(request, "walk/index.html", {"walks": walks, "walked_distance": total, "goal_distance": goal_km,
                                               "points": points})


@login_required()
def dashboard(request):
    walks = get_walks(request)
    chart_labels, chart_data = walk_bar_chart(walks)
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