from django.db import models

class Metrics(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu = models.FloatField()
    memory = models.FloatField()
    storage = models.FloatField()

    def __str__(self):
        return f"Metrics at {self.timestamp}"