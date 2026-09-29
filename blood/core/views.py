from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DonorProfile
from .models import BloodRequest



def home(request):
    return render(request, "home.html")


def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm = request.POST["confirm_password"]

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration Successful")
        return redirect("login")

    return render(request, "register.html")


def user_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "dashboard.html")



@login_required
def donor_profile(request):

    if request.method == "POST":

        phone = request.POST["phone"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        blood_group = request.POST["blood_group"]
        city = request.POST["city"]
        address = request.POST["address"]
        if DonorProfile.objects.filter(user=request.user).exists():
            messages.warning(request, "You already have a donor profile.")
            return redirect("dashboard")

        DonorProfile.objects.create(
            user=request.user,
            phone=phone,
            age=age,
            gender=gender,
            blood_group=blood_group,
            city=city,
            address=address,
            available=True
        )

        messages.success(request, "Donor Profile Created Successfully")

        return redirect("dashboard")

    return render(request, "donor_profile.html")


def user_logout(request):

    logout(request)

    return redirect("login")




@login_required
def search_donor(request):

    donors = None

    if request.method == "POST":

        blood_group = request.POST["blood_group"]

        city = request.POST["city"]

        donors = DonorProfile.objects.filter(
            blood_group=blood_group,
            city__iexact=city,
            available=True
        )

    return render(
        request,
        "search.html",
        {"donors": donors}
    )

@login_required
def send_request(request,donor_id):

    donor = DonorProfile.objects.get(id=donor_id)
    if donor.user == request.user:
        messages.error(request, "You cannot request blood from yourself.")
        return redirect("search")
    if BloodRequest.objects.filter(
        requester=request.user,
        donor=donor,
        status="Pending"
    ).exists():
        messages.warning(
        request,
        "You already have a pending request for this donor."
    )

        return redirect("search")

    if request.method == "POST":

        BloodRequest.objects.create(

            requester=request.user,

            donor=donor,

            patient_name=request.POST["patient_name"],

            blood_group=donor.blood_group,

            city=request.POST["city"],

            hospital=request.POST["hospital"],

            contact=request.POST["contact"]

        )

        messages.success(request, "Blood Request Sent Successfully")

        return redirect("search")

    return render(request, "request.html", {"donor": donor})
@login_required
def my_requests(request):

    requests = BloodRequest.objects.filter(
        requester=request.user
    )

    return render(
        request,
        "my_requests.html",
        {"requests": requests}
    )
@login_required
def received_requests(request):

    donor = DonorProfile.objects.get(user=request.user)

    requests = BloodRequest.objects.filter(
        donor=donor
    )

    return render(
        request,
        "received_requests.html",
        {"requests": requests}
    )
@login_required
def update_request(request, request_id, status):

    blood_request = get_object_or_404(
        BloodRequest,
        id=request_id
    )

    if blood_request.donor.user != request.user:

        messages.error(
            request,
            "You are not authorized."
        )

        return redirect("dashboard")

    blood_request.status = status

    blood_request.save()

    messages.success(
        request,
        "Request updated successfully."
    )

    return redirect("received_requests")

from django.shortcuts import get_object_or_404

@login_required
def edit_profile(request):
    donor = get_object_or_404(DonorProfile, user=request.user)

    if request.method == "POST":
        donor.phone = request.POST["phone"]
        donor.age = request.POST["age"]
        donor.gender = request.POST["gender"]
        donor.blood_group = request.POST["blood_group"]
        donor.city = request.POST["city"]
        donor.address = request.POST["address"]
        donor.available = "available" in request.POST

        donor.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("dashboard")

    return render(request, "edit_profile.html", {"donor": donor})

