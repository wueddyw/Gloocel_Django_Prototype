from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from .serializers import PersonSerializer
import datetime

"""
Registers a user if they are (Haven't tested, don't know how
to format the JSON on postman with the current model)
"""
class RegisterAPI(generics.GenericAPIView):
    """
    Checks if the user.is_staff before allowing them to 
    create an account
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = PersonSerializer(data = request.data)

        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'error': True,
                'error_msg': serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

"""
Logs a user in by creating a token, or refreshing their
token if they are already logged in
"""
class LoginAPI(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not User.objects.filter(username=request.data.get('username')).exists():
            return Response('Username does not exist', status=status.HTTP_404_NOT_FOUND)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
            
        token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])

        if not created:
            token.created = datetime.datetime.utcnow()
            token.save()

        return Response({'token': token.key})  

login_api = LoginAPI.as_view()


"""
Logs a user out and deletes their token from the database
"""
class LogoutAPI(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

"""
Verifies if the user's token is valid. Returns 200 response 
if valid, otherwise it will return a 401 response
"""
class VerifyAPI(APIView):
    def get(self, request, format=None):
        """
        Technically never reaches these conditions as the 
        'rest_framework.authentication.TokenAuthentication' handles it,
        but I implemented it incase you wanted to add additional responses
        or switch away from the rest framework's token authentication
        """
        if request.auth == None:
            content = 'No authentication token detected'
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        elif not request.user == Token.objects.get(key=request.auth).user:
            content = 'Incorrect user or token'
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response('Successfully authenticated', status=status.HTTP_200_OK)
