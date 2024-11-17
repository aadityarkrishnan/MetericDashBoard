import pika
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
import time
import logging
import os
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def create_connection():
    print("HELLO1...")
    """Establish a connection to RabbitMQ using environment variables."""
    logger.info("Setting up RabbitMQ connection parameters...")
    credentials = pika.PlainCredentials(
        os.getenv('RABBITMQ_USER', 'guest'),
        os.getenv('RABBITMQ_PASS', 'guest')
    )
    print("HELLO2...")
    parameters = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'rabbitmq'),
        port=int(os.getenv('RABBITMQ_PORT', 5672)),
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300,
        connection_attempts=3,
        retry_delay=5
    )
    print("HELLO3...")
    logger.debug(f"Connection parameters: {parameters}")
    return pika.BlockingConnection(parameters)


def callback(ch, method, properties, body):
    """Process and broadcast messages received from RabbitMQ."""
    try:
        logger.debug(f"Received message with body: {body}")
        metrics = json.loads(body)
        print("HELLO4...")

        # Cache the latest metrics
        cache.set("latest_metrics", metrics, timeout=300)
        logger.debug(f"Cached latest metrics: {metrics}")

        print("HELLO5...")

        # Broadcast to WebSocket group
        channel_layer = get_channel_layer()
        print("HELLO6...")
        async_to_sync(channel_layer.group_send)(
            "metrics_group",
            {
                "type": "send_metrics",
                "data": metrics
            }
        )
        print("HELLO7...")
        logger.info(f"Broadcasted metrics: {metrics}")
    except Exception as e:
        print("HELLO8...")
        logger.error(f"Error processing message: {e}")


def start_consumer():
    print("HELLO0...")
    """Start the RabbitMQ consumer and handle reconnections."""
    retry_interval = 5  # Start retry interval
    while True:
        try:
            print("HELLO9...")
            logger.info("Attempting to connect to RabbitMQ...")
            connection = create_connection()
            channel = connection.channel()
            print("HELLO10...")

            # Declare the queue (idempotent operation)
            logger.debug("Declaring 'ec2_metrics' queue...")
            channel.queue_declare(queue='ec2_metrics', durable=True)
            print("HELLO11...")

            # Set QoS
            logger.debug("Setting QoS (prefetch_count=1)...")
            channel.basic_qos(prefetch_count=1)
            print("HELLO12...")

            # Set up consumer
            logger.info("Setting up message consumer...")
            channel.basic_consume(
                queue='ec2_metrics',
                on_message_callback=callback,
                auto_ack=True
            )
            print("HELLO13...")

            logger.info('Connected! Waiting for metrics...')
            channel.start_consuming()
            print("HELLO14...")

        except pika.exceptions.AMQPConnectionError as conn_error:
            logger.error(f"Connection error: {conn_error}")
            print("HELLO15...")
        except pika.exceptions.ChannelClosedByBroker as channel_error:
            logger.error(f"Channel error: {channel_error}")
            print("HELLO16...")
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
            print("HELLO17...")
            if 'connection' in locals() and connection.is_open:
                connection.close()
                print("HELLO18...")
            break
        except Exception as e:
            print("HELLO19...")
            logger.error(f"Unexpected error: {e}")
        finally:
            print("HELLO20...")
            # Exponential backoff with jitter
            retry_interval = min(retry_interval * 2, 60)  # Capped at 60 seconds
            jitter = random.uniform(0, 1)
            logger.info(f"Retrying in {retry_interval + jitter:.2f} seconds...")
            time.sleep(retry_interval + jitter)


if __name__ == "__main__":
    print("..................9...")
    logger.info("Starting RabbitMQ consumer...")
    print("#################################################################")
    start_consumer()
