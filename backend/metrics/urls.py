from django.urls import path
from .views import metrics_view
print("INSIDE SUB URL")
urlpatterns = [
    path('metrics/', metrics_view, name='metrics-api'),
]