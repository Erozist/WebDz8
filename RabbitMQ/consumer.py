import pika
import json
import time
import logging
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

def send_email_stub(contact):
    """Імітація відправки email з затримкою"""
    logger.info(f"Надсилається email до {contact.email}...")
    time.sleep(2)  # Імітація затримки на 2 секунди
    logger.info(f"Email надіслано до {contact.email}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    contact = Contact.objects(id=contact_id).first()

    if contact and not contact.is_sent:
        send_email_stub(contact)
        contact.is_sent = True
        contact.save()
        logger.info(f"Email надіслано до {contact.fullname} ({contact.email})")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

logger.info('Очікування повідомлень. Натисніть Ctrl+C для виходу.')
channel.start_consuming()
