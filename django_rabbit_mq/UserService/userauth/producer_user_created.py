import json
import pika

ROUTING_KEY = 'user.created,key'
EXCHANGE = 'user_exchange'
THREADS = 5


class ProducerUserCreated:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300)
        )
        self.channel = self.connection.channel()

    def publish(self, method, body):
        print("inside UserService: Sending to RabbitMQ")
        print(body)
        properties = pika.BasicProperties(method)
        self.channel.basic_publish(exchange=EXCHANGE, routing_key=ROUTING_KEY,
                                   body=json.dumps(body), properties=properties)
