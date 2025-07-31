# serializers.py
from rest_framework import serializers
from .models import AcademicEvent

class AcademicEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicEvent
        fields = '__all__'
