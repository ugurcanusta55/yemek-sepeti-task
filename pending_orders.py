import pika, sys, os, json
from db import models

from db.database import SessionLocal as Session

# an Engine, which the Session will use for connection
# resources

def main():
    print("RABBITMQ_HOST", os.getenv('RABBITMQ_HOST', 'rabbitmq'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST', 'rabbitmq')))
    channel = connection.channel()

    channel.queue_declare(queue='pending_orders')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print("data", data)
        with Session.begin() as session:
            order = models.Order()
            food_id = [food for food in data['food']]
            print("food_id", food_id)
            foods = session.query(models.Food).filter(models.Food.id.in_(food_id)).all()
            print("foods", foods)
            for food in foods:
                order.food.append(food)
            order.owner_id = data['owner_id']
            session.add(order)
            session.commit()
            print(" [x] Received %r" % body)

    channel.basic_consume(queue='pending_orders', on_message_callback=callback, auto_ack=True)

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