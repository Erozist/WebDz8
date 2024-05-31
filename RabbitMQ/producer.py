import pika
import json
import logging
from faker import Faker
from models import Contact
from mongoengine import connect

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Налаштування RabbitMQ
rabbitmq_host = 'localhost'
queue_name = 'email_queue'

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue=queue_name)

# Генерація фейкових контактів
fake = Faker()

def generate_contacts(num_contacts):
    contacts = []
    for _ in range(num_contacts):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            address=fake.address()
        )
        contact.save()
        contacts.append(contact)
    return contacts

def main():
    connect('contacts_db', host='localhost', port=27017)
    num_contacts = 10
    contacts = generate_contacts(num_contacts)

    for contact in contacts:
        message = {'contact_id': str(contact.id)}
        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
        logger.info(f"Контакт {contact.fullname} додано до черги.")

    connection.close()
    logger.info(f'{num_contacts} контакти згенеровано та додано в чергу.')

if __name__ == "__main__":
    main()
