from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Student


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("admission_form")
        else:
            return render(request, "admission/login.html", {
                "error": "Invalid Username or Password"
            })

    return render(request, "admission/login.html")


@login_required
def admission_form(request):
    return render(request, "form.html")


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


def update_status(request, student_id, status):
    student = get_object_or_404(Student, id=student_id)
    student.status = status
    student.save()
    return redirect("dashboard")


def check_status(request):
    students = Student.objects.all()
    return render(request, "admission/check_status.html", {"students": students})


def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "admission/student_detail.html", {"student": student})


def download_receipt(request, id):
    student = get_object_or_404(Student, id=id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="receipt_{student.id}.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, "ADMISSION RECEIPT")
    p.drawString(100, 760, f"ID: {student.id}")
    p.drawString(100, 740, f"Name: {student.name}")
    p.drawString(100, 720, f"Course: {student.course}")
    p.drawString(100, 700, f"Email: {student.email}")
    p.drawString(100, 680, f"Phone: {student.phone}")

    p.save()

    return response


def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("dashboard")


def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.phone = request.POST.get("phone")
        student.course = request.POST.get("course")

        student.save()
        return redirect("dashboard")

    return render(
        request,
        "admission/edit_student.html",
        {"student": student},
    )