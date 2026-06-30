from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)

    address = models.TextField()
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=20)
    marksheet = models.FileField(upload_to='marksheets/', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    fees_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    fees_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    @property
    def fees_balance(self):
        return self.fees_amount - self.fees_paid

    def __str__(self):
        return self.name