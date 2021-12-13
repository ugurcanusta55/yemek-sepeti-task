import pika, sys, os, json
from db import models
from db.database import SessionLocal as Session

def main():
    print("RABBITMQ_HOST", os.getenv('RABBITMQ_HOST', 'rabbitmq'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST', 'rabbitmq')))
    channel = connection.channel()

    channel.queue_declare(queue='confirmed_orders')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        data = json.loads(body)
        print("data", data)
        order_id = data['order_id']
        with Session.begin() as session:
            session.query(models.Order).filter(models.Order.id==int(order_id)).update({"is_confirmed": True})
            session.commit()

    channel.basic_consume(queue='confirmed_orders', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)