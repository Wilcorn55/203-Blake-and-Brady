from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from faunadb import query as q
import pytz
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import hashlib
import datetime

client = FaunaClient(secret="fnAEnqvWm6ACU1hu8c8rIhsZDvTfg94om1Ecwz9P")

indexes = client.query(q.paginate(q.indexes()))

def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hello! {username}, your account has been created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'users/profile.html')



def create_CV(request):
    if request.method == "POST":
        username = request.session["user"]["username"]
        full_name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        about_you = request.POST.get("about_you")
        career = request.POST.get("career")
        education = request.POST.get("education")
        job_1_start = request.POST.get("job_1_start")
        job_1_end = request.POST.get("job_1_end")
        job_1_details = request.POST.get("job_1_details")
        job_2_start = request.POST.get("job_2_start")
        job_2_end = request.POST.get("job_2_end")
        job_2_details = request.POST.get("job_2_details")
        job_3_start = request.POST.get("job_3_start")
        job_3_end = request.POST.get("job_3_end")
        job_3_details = request.POST.get("job_3_details")
        try:
            cv = client.query(q.get(q.match(q.index("cv_index"), username)))
            quiz = client.query(q.update(q.ref(q.collection("CV_Info"), cv["ref"].id()),
                                         {
                                             "data":
                                                 {
                                                     "user": username,
                                                     "full_name": full_name,
                                                     "address": address,
                                                     "phone": phone,
                                                     "email": email,
                                                     "about_you": about_you,
                                                     "education": education,
                                                     "career": career,
                                                     "job_1_start": job_1_start,
                                                     "job_1_end": job_1_end,
                                                     "job_1_details": job_1_details,
                                                     "job_2_start": job_2_start,
                                                     "job_2_end": job_2_end,
                                                     "job_2_details": job_2_details,
                                                     "job_3_start": job_3_start,
                                                     "job_3_end": job_3_end,
                                                     "job_3_details": job_3_details,
                                                 }
                                         }))
            messages.add_message(request, messages.INFO, 'CV Successfully Edited. Download CV Now')
            return redirect('users/profile.html')
        except:
            quiz = client.query(q.create(q.collection("CV_Info"),
                                         {
                                             "data":
                                                 {
                                                     "user": username,
                                                     "full_name": full_name,
                                                     "address": address,
                                                     "phone": phone,
                                                     "email": email,
                                                     "about_you": about_you,
                                                     "education": education,
                                                     "career": career,
                                                     "job_1_start": job_1_start,
                                                     "job_1_end": job_1_end,
                                                     "job_1_details": job_1_details,
                                                     "job_2_start": job_2_start,
                                                     "job_2_end": job_2_end,
                                                     "job_2_details": job_2_details,
                                                     "job_3_start": job_3_start,
                                                     "job_3_end": job_3_end,
                                                     "job_3_details": job_3_details,
                                                 }
                                         }))
            messages.add_message(request, messages.INFO, 'CV Successfully Saved. View CV Now')
            return redirect()  #Link to CV Page Here
        else:
            try:
                CV_info = client.query(q.get(q.match(q.index("CV_index"), request.session["user"]["username"])))["data"]
                context={"CV_info":CV_info}
                return render(request,"create-CV.html",context)
            except:
                return render(request,"create-CV.html")
