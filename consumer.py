import pika
from models import Contact
from bson import ObjectId

import connect_to_mongo_db


def main():

    connect_to_mongo_db

    # Настройка RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    def callback(ch, method, properties, body):
        contact_id = ObjectId(body.decode())
        contact = Contact.objects(id=contact_id).first()
        if contact:
            print(f"Message sent to {contact.fullname} - {contact_id}")
            contact.send_email = True
            contact.save()

    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
     main()