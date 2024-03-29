import json
import pika
import threading

ROUTING_KEY = 'user.created.key'
EXCHANGE = 'user_exchange'
THREADS = 5


class UserQueueListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'
        ))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')
        result = self.channel.queue_declare(exclusive=True, queue='')
        queue_name = result.method.queue
        self.channel.queue_bind(queue=queue_name, exchange=EXCHANGE, routing_key=ROUTING_KEY)
        self.channel.basic_qos(prefetch_count=THREADS * 10)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)

    def callback(self, channel, method, properties, body):
        # print(properties.content_type)
        # print(method)
        message = json.loads(body)
        if properties.content_type == "user_created_method":
            print(message)
        if properties.content_type == "product_created_method":
            print(message)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print('Inside LoggingService:  Created Listener ')
        self.channel.start_consuming()
