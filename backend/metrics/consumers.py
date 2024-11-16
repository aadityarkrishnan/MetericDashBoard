# backend/metrics/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MetricsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "metrics_group"
        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from group
    async def send_metrics(self, event):
        metrics = event['data']
        await self.send(text_data=json.dumps(metrics))
