from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from faunadb import query as q
import pytz
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import hashlib
import datetime

def home(request):
    return HttpResponse("<h1>Home</h1>")


# Create your views here.
