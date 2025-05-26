import pika


class RabbitMQClient:
    """RabbitMQ 클라이언트를 구현하여 메시지 발행 및 소비를 위한 유틸리티를 제공합니다."""

    def __init__(self, host="localhost") -> None:
        self.host = host
        self.connection = None
        self.channel = None

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self.channel = self.connection.channel()

    def declare_queue(self, queue_name):
        self.connect()
        self.channel.queue_declare(queue=queue_name, durable=True)

    def publish_message(self, queue_name, message):
        self.connect()
        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),  # Make message persistent
        )

    def consume_messages(self, queue_name, callback):
        self.connect()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        self.channel.start_consuming()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
