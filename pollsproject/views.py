```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from .forms import StudentForm
from .models import Student


def admission_form(request):

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')

    else:
        form = StudentForm()

    return render(
        request,
        'admission/form.html',
        {'form': form}
    )


def success(request):

    return render(
        request,
        'admission/success.html'
    )


def dashboard(request):

    search = request.GET.get('search')

    if search:
        students = Student.objects.filter(
            name__icontains=search
        )
    else:
        students = Student.objects.all()

    total_students = Student.objects.count()

    pending_students = Student.objects.filter(
        status='Pending'
    ).count()

    approved_students = Student.objects.filter(
        status='Approved'
    ).count()

    rejected_students = Student.objects.filter(
        status='Rejected'
    ).count()

    context = {
        'students': students,
        'total_students': total_students,
        'pending_students': pending_students,
        'approved_students': approved_students,
        'rejected_students': rejected_students,
    }

    return render(
        request,
        'admission/dashboard.html',
        context
    )

def update_status(request, student_id, status):

    student = Student.objects.get(id=student_id)

    student.status = status

    student.save()

    return redirect('dashboard')


def check_status(request):

    student = None

    if request.method == 'POST':

        application_no = request.POST.get(
            'application_no'
        )

        try:
            student = Student.objects.get(
                application_no=application_no
            )

        except Student.DoesNotExist:
            student = None

    return render(
        request,
        'admission/check_status.html',
        {'student': student}
    )


def generate_pdf(request, student_id):

    student = Student.objects.get(
        id=student_id
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        f'attachment; filename='
        f'{student.application_no}.pdf'
    )

    pdf = canvas.Canvas(response)

    pdf.setTitle(
        "Admission Receipt"
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        180,
        800,
        "Admission Receipt"
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        100,
        740,
        f"Application No : {student.application_no}"
    )

    pdf.drawString(
        100,
        710,
        f"Name : {student.name}"
    )

    pdf.drawString(
        100,
        680,
        f"Course : {student.course}"
    )

    pdf.drawString(
        100,
        650,
        f"Phone : {student.phone}"
    )

    pdf.drawString(
        100,
        620,
        f"Email : {student.email}"
    )

    pdf.drawString(
        100,
        590,
        f"Status : {student.status}"
    )

    pdf.drawString(
        100,
        540,
        "Thank You For Applying"
    )

    pdf.save()

    return response
```
