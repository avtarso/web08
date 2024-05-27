import pika
from models import Contact

import connect_to_mongo_db

def main():

    # Setup RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    # connect to MongoDB
    connect_to_mongo_db

    # Get data from MongoDB
    contacts = Contact.objects(send_email=False)

    for contact in contacts:
        message = str(contact.id)
        channel.basic_publish(exchange='',
                            routing_key='email_queue',
                            body=message)
        print(f"Message sent for contact {contact.fullname} - {message}")

    connection.close()


if __name__ == "__main__":
    
    main():