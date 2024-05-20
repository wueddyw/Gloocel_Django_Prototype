from django.db import models
from rest_framework_api_key.models import APIKey
from door.models import Door

class Device(models.Model):

  def key_default(myName):
    api_key, key = APIKey.objects.create_key(name=myName)
    return key

  device_name = models.CharField(max_length=255, primary_key=True)
  device_type = models.CharField(max_length=30)
  api_key = models.CharField(max_length=255, blank=True, null=True, editable=False)
  door = models.ForeignKey(Door, related_name='Door', null=True, on_delete=models.CASCADE)


  def __str__(self):
    return self.device_name

  def save(self, *args, **kwargs):
    self.api_key = Device.key_default(self.device_name)
    super().save(*args, **kwargs)
    """
      TODO: 
        Create a message queue when a device is created
        API endpoint on the backend server will allow a device to poll
        if this message queue has any messages, if there is a message
        the message will be extracted from the message queue
    """
    # createMessageQueue(self.device_name)

  def delete(self, *args, **kwargs):
    #self.api_key = Device.key_default(self.device_name)
    super().save(*args, **kwargs)
    """
      TODO: 
        Create a message queue when a device is created
        API endpoint on the backend server will allow a device to poll
        if this message queue has any messages, if there is a message
        the message will be extracted from the message queue
    """
    # createMessageQueue(self.device_name)
