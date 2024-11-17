from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
from .models import Metrics

@api_view(['GET'])
def metrics_view(request):
    print("IN THE GET FN")
    try:
        # Fetch cached metrics
        print("METRICS BEFORE")
        metrics = cache.get("latest_metrics")
        print("METRICS AFTER")
        print(metrics)

        if not metrics:
            # If cache is empty, fetch the latest from DB or return default
            latest = Metrics.objects.order_by('-timestamp').first()
            if latest:
                metrics = {
                    "cpu": latest.cpu,
                    "memory": latest.memory,
                    "storage": latest.storage,
                    "timestamp": latest.timestamp,
                }
            else:
                metrics = {"cpu": 0, "memory": 0, "storage": 0, "timestamp": None}

        return Response(metrics)

    except Exception as e:
        print("Exception in metrics_view")
        print(e)
        # Handle any unexpected errors
        return Response({"error": str(e)}, status=500)

