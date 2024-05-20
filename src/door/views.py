from django.http import Http404
from django.shortcuts import render
from .models import Door
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DoorSerializer
import json
import pika
import os
from dotenv import load_dotenv
from datetime import datetime

# Environment Variables 
load_dotenv()

RMQ_USER = os.getenv('RMQ_USER')
PASS = os.getenv('RMQ_PASS')
IP = os.getenv('RMQ_IP')
PORT = os.getenv('RMQ_PORT')
CREDENTIALS = pika.PlainCredentials(RMQ_USER, PASS)

class DoorList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
 queryset = Door.objects.all()
 serializer_class = DoorSerializer

 """
 Returns a list of all doors
 """
 def get(self, request, *args, **kwargs):
  return self.list(request, *args, **kwargs)


class DoorOpen(APIView):
 connection = pika.BlockingConnection(pika.ConnectionParameters(IP, PORT, '/', CREDENTIALS))
 channel = connection.channel()
 channel.confirm_delivery()

 """
 Adds a message to the target door's message queue
 """
 def load_queue(self, door):
  
  try:
   if not self.connection or self.connection.is_closed:
    print("Connection with RabbitMQ has ended... reconnected")
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(IP, PORT, '/', CREDENTIALS))
    self.channel = self.connection.channel()

   now = datetime.now()
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   message = "OPEN DOOR Message sent: {}".format(dt_string)

   self.channel.basic_publish(exchange='',
   routing_key=door.door_name,
   body=message, mandatory=True)

   return {
    'success': 'Added a message request to ' + door.door_name + ' ' + message
   }
  except Exception as e:
   return {
    "error": str(e)
   }

 """
 Get an instance of the Door from the database
 """
 def get_door(self, pk):
  try:
   return Door.objects.get(pk=pk)
  except Door.DoesNotExist:
   raise Http404

 """
 Uses the JSON data to send a message to a door's message queue
 """
 def post(self, request, pk, format=None):
  door = self.get_door(pk)
  response = self.load_queue(door)
  return Response(response)
