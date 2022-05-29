

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "App"

urlpatterns = [
    path("", views.login, name="login"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("index", views.index, name="index"),
    path("create-cv", views.create_cv, name="create-cv"),
    path("cv", views.cv, name="cv"),

]
