"""
views.py — HTTP request handlers for AttendanceChimp.

Each view corresponds to one URL endpoint.  Views receive an HTTP request,
interact with the database via models.py, and return an HTTP response.
"""

from django.shortcuts import render, redirect
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseBadRequest, JsonResponse)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
import zoneinfo
import json
import io

from .models import (
    InstructorProfile,
    StudentProfile,
    Course,
    Enrollment,
    Lecture,
    QRCodeUpload,
    generate_qr_identifier
)

import uuid
CDT = zoneinfo.ZoneInfo("America/Chicago")


# ---------------------------------------------------------------------------
# HW2  — index, time, sum
# ---------------------------------------------------------------------------

def index(request):
    """Render the home page (index.html)."""

    now = datetime.now(CDT).strftime("%H:%M")

    context = {
        "current_time": now,
        "current_user": request.user
    }

    return render(request, 'app/index.html', context)






# ---------------------------------------------------------------------------
# HW4  — user creation
# ---------------------------------------------------------------------------
def new(request):
    """Display the signup form."""

    if request.method != "GET":
        return HttpResponse(status=405)

    return render(request, 'app/new.html')

@csrf_exempt
def createUser(request):
    """Create a new student or instructor account."""

    if request.method != "POST":
        return HttpResponse(status=405)

    user_name = request.POST.get("user_name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    role = request.POST.get("is_student")

    if not user_name or not email or not password:
        return HttpResponse("Missing required information", status=400)

    if role not in ["student", "instructor"]:
        return HttpResponse("Invalid account type", status=400)

    if User.objects.filter(email__iexact=email).exists():
        return HttpResponse("Email already exists", status=400)

    if User.objects.filter(username=user_name).exists():
        return HttpResponse("Username already exists", status=400)

    user = User.objects.create_user(
        username=user_name,
        email=email,
        password=password
    )

    if role == "student":
        StudentProfile.objects.create(
            user=user,
            student_id=uuid.uuid4().hex[:20]
        )
    else:
        InstructorProfile.objects.create(user=user)

    login(request, user)

    return HttpResponse("User created successfully", status=200)


# ---------------------------------------------------------------------------
# HW5  — courses, lectures, QR uploads, dump
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# HW6  — getUploads
# ---------------------------------------------------------------------------





from datetime import datetime
from zoneinfo import ZoneInfo
from django.http import HttpResponse, JsonResponse


def time_view(request):
    now = datetime.now(ZoneInfo("America/Chicago"))
    return HttpResponse(now.strftime("%H:%M"), content_type="text/plain")


def sum_view(request):
    def to_number(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    try:
        n1 = to_number(request.GET.get("n1"))
        n2 = to_number(request.GET.get("n2"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "n1 and n2 must be numbers"}, status=400)
    return JsonResponse({"sum": n1 + n2})


import json


def sum_view(request):
    def to_number(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    try:
        n1 = to_number(request.GET.get("n1"))
        n2 = to_number(request.GET.get("n2"))
    except (TypeError, ValueError):
        return HttpResponse("<p>n1 and n2 must be numbers</p>", status=400)
    return HttpResponse("<p>" + json.dumps({"sum": n1 + n2}) + "</p>")


from decimal import Decimal


def sum_view(request):
    try:
        total = Decimal(request.GET.get("n1")) + Decimal(request.GET.get("n2"))
    except (TypeError, ArithmeticError):
        return HttpResponse("<p>n1 and n2 must be numbers</p>", status=400)
    return HttpResponse("<p>" + str(total) + "</p>")


from decimal import Decimal


def sum_view(request):
    try:
        total = Decimal(request.GET.get("n1")) + Decimal(request.GET.get("n2"))
    except (TypeError, ArithmeticError):
        return HttpResponse("<p>n1 and n2 must be numbers</p>", status=400)
    return HttpResponse("<p>" + str(total) + "</p>")
