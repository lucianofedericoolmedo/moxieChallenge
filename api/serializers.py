from datetime import time, timedelta
from rest_framework import serializers
from .models import MedSpa, Service, Appointment, AppointmentStatus

class MedSpaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedSpa
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
    med_spa = serializers.PrimaryKeyRelatedField(queryset=MedSpa.objects.all(), many=False)

    class Meta:
        model = Appointment
        fields = ['id', 'start_time', 'status', 'med_spa', 'services']
        read_only = ['total_duration', 'total_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        self.fields['status'].read_only = self.is_post()
    
    def is_post(self):
        request = self.context.get('request', None)
        return request and request.method == 'POST'

    def is_patch(self):
        request = self.context.get('request', None)
        return request and request.method == 'PATCH'

    def to_representation(self, instance):
        """Customize the representation of the Appointment instance."""
        representation = super().to_representation(instance)
        if not self.is_post() and not self.is_patch():
            representation['services'] = ServiceSerializer(instance.services.all(), many=True).data
            representation['med_spa'] = MedSpaSerializer(instance.med_spa, read_only=True).data
        representation['total_duration'] = instance.total_duration
        representation['total_price'] = instance.total_price
        return representation

    def validate_start_time(self, value):
        start_office_hour = time(9, 0)  # 9 AM
        end_office_hour = time(18, 0)  # 6 PM

        if value.time() < start_office_hour or value.time() > end_office_hour:
            raise serializers.ValidationError("Appointment start time must be between 9 AM and 6 PM.")
        return value

    def validate(self, data):
        has_status = 'status' in data
        if has_status:
            current_status = self.instance.status if self.instance else None
            new_status = data['status']
            # Validate status transitions
            if current_status == 'COMPLETED' or current_status == 'CANCELLED':
                raise serializers.ValidationError("Cannot change status for COMPLETED or CANCELLED.")
            if current_status == 'SCHEDULED':
                if new_status not in ['CANCELLED', 'COMPLETED']:
                    raise serializers.ValidationError("Invalid status change. Only CANCELLED or COMPLETED are allowed from SCHEDULED.")
        
        # Check if the expected end time exceeds 6 PM
        end_office_hour = time(18, 0)  # 6 PM
        if self.is_post():
            total_duration = data['start_time'] + timedelta(minutes=sum([service.duration for service in data['services']]))
            if total_duration.time() > end_office_hour:
                raise serializers.ValidationError("The sum of start time and total duration of services must not exceed 6 PM.")
        return data

    def create(self, validated_data):
        services = validated_data.pop('services')
        # Remove 'status' from validated_data to prevent it from being set on creation
        if self.is_post():
            if 'status' in validated_data:
                validated_data.pop('status')  # Ensure status is not included on creation
            validated_data['status'] = AppointmentStatus.SCHEDULED

        validated_data['total_duration'] = sum(service.duration for service in services)
        validated_data['total_price'] = sum(service.price for service in services)
        appointment = Appointment.objects.create(**validated_data)

        # Add services to the appointment
        appointment.services.set(services)

        return appointment
