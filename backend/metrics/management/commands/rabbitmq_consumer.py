# backend/metrics/management/commands/rabbitmq_consumer.py

from django.core.management.base import BaseCommand
from metrics.rabbitmq_consumer import start_consumer

class Command(BaseCommand):
    help = 'Starts the RabbitMQ consumer'

    def handle(self, *args, **kwargs):
        start_consumer()
