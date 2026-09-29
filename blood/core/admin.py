from django.contrib import admin
from .models import DonorProfile, BloodRequest

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "blood_group",
        "city",
        "available",
    )

    search_fields = (
        "user__username",
        "city",
        "blood_group",
    )

    list_filter = (
        "blood_group",
        "available",
        "city",
    )


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name",
        "requester",
        "donor",
        "status",
        "request_date",
    )

    search_fields = (
        "patient_name",
        "hospital",
    )

    list_filter = (
        "status",
        "blood_group",
    )