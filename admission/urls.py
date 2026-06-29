from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),
    
    path(
    'admission/',
    views.admission_form,
    name='admission_form'
),

    path(
        'success/',
        views.success,
        name='success'
    ),
      

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'status/<int:student_id>/<str:status>/',
        views.update_status,
        name='update_status'
    ),

    path(
        'check-status/',
        views.check_status,
        name='check_status'
    ),
path(
    'student/<int:id>/',
    views.student_detail,
    name='student_detail'
),
    path(
    'receipt/<int:id>/',
    views.download_receipt,
    name='download_receipt'
),
path(
    'delete/<int:id>/',
    views.delete_student,
    name='delete_student'
),
path(
'edit/<int:id>/',
views.edit_student,
name='edit_student'
),


]
