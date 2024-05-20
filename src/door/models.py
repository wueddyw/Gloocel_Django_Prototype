import os
from django.db import models
from location.models import Location
from django.db.models.signals import pre_save
from dotenv import load_dotenv
import pika 
from dotenv import load_dotenv

# Environment Variables 
load_dotenv()

RMQ_USER = os.getenv('RMQ_USER')
PASS = os.getenv('RMQ_PASS')
IP = os.getenv('RMQ_IP')
PORT = os.getenv('RMQ_PORT')

class Door(models.Model):
 door_name = models.CharField(max_length = 50, null= True, unique=True)
 door_type = models.CharField(max_length = 30)
 location = models.ForeignKey(Location, related_name='Location_Door', null=True, on_delete=models.CASCADE)
 message = models.CharField(max_length=255, editable=False, default=None, blank=True, null=True)

 def __str__(self):
  return self.door_name + ' | ' + str(self.location)

# Created Queue function that creates a rabbitMQ queue when the mode is created 
def create_queue(sender, instance, **kwargs):
  print("Done saving an instance now creating a queue")
  
  # connection needs to be changed according to rabbitMQ
  credentials = pika.PlainCredentials(RMQ_USER, PASS)
  connection = pika.BlockingConnection(pika.ConnectionParameters(IP, PORT, '/', credentials))
  channel = connection.channel()

  # creates queue on rabbitmq with the name of the door
  msg_table = channel.queue_declare(queue=instance.door_name)
  instance.message = msg_table

pre_save.connect(create_queue, sender=Door)



