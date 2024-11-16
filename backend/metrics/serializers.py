# backend/metrics/serializers.py

from rest_framework import serializers
from .models import Metrics

class MetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrics
        fields = ['cpu', 'memory', 'storage', 'timestamp']
