import pika
import os
import json

def create_order(order):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST')))
    channel = connection.channel()

    channel.queue_declare(queue="pending_orders")
    channel.basic_publish(exchange='', routing_key='pending_orders', body=json.dumps(order.dict()))
    connection.close()


def confirm_orders(order_id):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST')))
    channel = connection.channel()

    channel.queue_declare(queue="confirmed_orders")

    channel.basic_publish(exchange='', routing_key='confirmed_orders', body=json.dumps(order_id))
    connection.close()
