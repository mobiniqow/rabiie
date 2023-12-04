import socket
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EVENT


class EventSocket(APIView):

    def post(self, request):
        address = request.data.get('address')
        port = request.data.get('port')
        message = request.data.get('message')
        EVENT()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((address, port))
            sock.sendall(message.encode())
            sock.close()
            return Response("Message sent successfully!", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
