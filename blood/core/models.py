from django.db import models
from django.contrib.auth.models import User


class DonorProfile(models.Model):

    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)

    age = models.PositiveIntegerField()

    gender = models.CharField(max_length=10, choices=GENDER)

    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)

    city = models.CharField(max_length=100)

    address = models.TextField()

    available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class BloodRequest(models.Model):

    STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requests_made"
    )

    donor = models.ForeignKey(
        DonorProfile,
        on_delete=models.CASCADE,
        related_name="requests_received"
    )

    patient_name = models.CharField(max_length=100)

    blood_group = models.CharField(max_length=5)

    city = models.CharField(max_length=100)

    hospital = models.CharField(max_length=150)

    contact = models.CharField(max_length=15)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name
