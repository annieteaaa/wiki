from django.urls import include, path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index),
    path("wiki/<str:title>", views.getentry, name="getentry"),
    path("<str:entry>", views.results, name="results"),
    path("new/newpage.html", views.newpage, name="newpage"),
    path("search/", views.search, name="search"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.randomPage, name="random"),
]
