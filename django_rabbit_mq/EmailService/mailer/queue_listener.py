import json
import pika
import threading

from paramiko import channel

ROUTING_KEY = 'user.created.key'
EXCHANGE = 'user_exchange'
THREADS = 5


class UserCreatedListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(queue=queue_name, exchange=EXCHANGE, routing_key=ROUTING_KEY)
        self.channel.basic_qos(prefetch_count=THREADS * 10)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)

    def callback(self, ch, method, properties, body):
        if properties.content_type == 'user_created_method':
            message = json.loads(body)
            print(message)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print('Inside LoggingService: Ctated Listener')
        self.channel.star_consuming()
