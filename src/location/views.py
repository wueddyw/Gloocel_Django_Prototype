from .models import Location
from .serializers import LocationSerializer
from rest_framework import mixins
from rest_framework import generics 


class LocationList(
 mixins.ListModelMixin,
 mixins.CreateModelMixin,
 generics.GenericAPIView):
  queryset = Location.objects.all()
  serializer_class = LocationSerializer

  """
  Returns a list of all the locations
  """
  def get(self, request, *args, **kwargs):
   return self.list(request, *args, **kwargs)

  """
  Commented out as we don't want users to be able to create
  new locations
  """
#   def post(self, request, *args, **kwargs):
#    return self.create(request, *args, **kwargs)


class LocationDetail(
 mixins.RetrieveModelMixin,
 mixins.UpdateModelMixin,
 mixins.DestroyModelMixin,
 generics.GenericAPIView):
  
  queryset = Location.objects.all()
  serializer_class = LocationSerializer

  """
  Returns the details of a specific location
  """
  def get(self, request, *args, **kwargs):
   return self.retrieve(request, *args, **kwargs)

  """
  Commented out as we don't want users to be able to update
  current locations
  """
#   def put(self, request, *args, **kwargs):
#    return self.update(request, *args, **kwargs)


  """
  Commented out as we don't want users to be able to delete
  current locations
  """
#   def delete(self, request, *args, **kwargs):
#    return self.destroy(request, *args, **kwargs)


