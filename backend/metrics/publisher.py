import pika
import json
import time
import psutil
import logging

# Set up logging for better debugging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def publish_metrics():
    retry_attempts = 5  # Number of retry attempts
    retry_delay = 70  # Delay between retries in seconds
    attempt = 0

    while attempt < retry_attempts:
        try:
            logger.debug(f"Attempt {attempt + 1} to connect to RabbitMQ...")

            credentials = pika.PlainCredentials('guest', 'guest')
            parameters = pika.ConnectionParameters(
                host="rabbitmq",  # Change this if necessary
                port=5672,
                credentials=credentials,
                heartbeat=600,
                connection_attempts=3,
                retry_delay=5
            )

            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            logger.debug("Successfully connected to RabbitMQ!")
            queue_name = 'ec2_metrics'
            channel.queue_declare(queue=queue_name, durable=True)

            logger.debug("Queue declared, starting metric publishing loop...")
            while True:
                metrics = {
                    'cpu': psutil.cpu_percent(interval=1),
                    'memory': psutil.virtual_memory().percent,
                    'storage': psutil.disk_usage('/').percent,
                    'timestamp': time.time(),
                }
                channel.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=json.dumps(metrics),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Make message persistent
                    )
                )
                logger.debug(f"Published metrics: {metrics}")
                time.sleep(100)

        except pika.exceptions.AMQPConnectionError as e:
            attempt += 1
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            if attempt < retry_attempts:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Max retry attempts reached. Exiting.")
                break

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            break

        finally:
            if 'connection' in locals() and connection.is_open:
                connection.close()
                logger.debug("Connection closed.")


if __name__ == "__main__":
    publish_metrics()
