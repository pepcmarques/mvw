from django.urls import path
from .views import home, dashboard, walk_chart, add_walk

app_name = "walk"

urlpatterns = [
    path("", home, name="home"),
    path('walk-chart/', walk_chart, name='walk-chart'),
    path("dashboard", dashboard, name="dashboard"),
    path("add-walk", add_walk, name="add-walk"),
]