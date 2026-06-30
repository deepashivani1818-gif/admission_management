from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from .models import Student
from .forms import StudentForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("admission_form")
        else:
            return render(
                request,
                "admission/login.html",
                {"error": "Invalid Username or Password"},
            )

    return render(request, "admission/login.html")


def admission_form(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("success")
        else:
            print(form.errors)

    else:
        form = StudentForm()

    return render(request, "admission/form.html", {"form": form})


def success(request):
    return render(request, "admission/success.html")


@login_required
def dashboard(request):
    q = request.GET.get("q")

    if q:
        students = Student.objects.filter(name__icontains=q)
    else:
        students = Student.objects.all()

    total = Student.objects.count()
    approved = Student.objects.filter(status="Approved").count()
    rejected = Student.objects.filter(status="Rejected").count()
    pending = Student.objects.filter(status="Pending").count()

    return render(
        request,
        "admission/dashboard.html",
        {
            "students": students,
            "total": total,
            "approved": approved,
            "rejected": rejected,
            "pending": pending,
        },
    )


@login_required
def update_status(request, student_id, status):
    student = get_object_or_404(Student, id=student_id)
    student.status = status
    student.save()
    return redirect("dashboard")


def check_status(request):
    students = Student.objects.all()
    return render(
        request,
        "admission/check_status.html",
        {"students": students},
    )


def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(
        request,
        "admission/student_detail.html",
        {"student": student},
    )


def download_receipt(request, id):
    student = get_object_or_404(Student, id=id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="receipt_{student.id}.pdf"'
    )

    p = canvas.Canvas(response)
    p.setTitle("Admission Receipt")

    p.drawString(100, 800, "STUDENT ADMISSION RECEIPT")
    p.drawString(100, 770, f"Student ID : {student.id}")
    p.drawString(100, 750, f"Name       : {student.name}")
    p.drawString(100, 730, f"Course     : {student.course}")
    p.drawString(100, 710, f"Email      : {student.email}")
    p.drawString(100, 690, f"Phone      : {student.phone}")
    p.drawString(100, 670, f"Status     : {student.status}")

    p.save()
    return response


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("dashboard")


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student,
        )

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "admission/edit_student.html",
        {
            "form": form,
            "student": student,
        },
    )