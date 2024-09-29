from django.contrib import admin
from api.models import MedSpa, Service, Appointment, AppointmentServiceRel

@admin.register(MedSpa)
class MedSpaAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email')
    search_fields = ('name', 'email')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'med_spa', 'price', 'duration')
    list_filter = ('med_spa',)
    search_fields = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('med_spa', 'start_time', 'status', 'total_duration', 'total_price')
    list_filter = ('med_spa', 'status', 'start_time')
    search_fields = ('med_spa__name',)

@admin.register(AppointmentServiceRel)
class AppointmentServiceRelAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'service')
    list_filter = ('appointment', 'service')
