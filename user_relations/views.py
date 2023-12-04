from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserChild
from account.models import User


class UserChildManipulation(APIView):
    def post(self, request):
        user_phone = request.data.get('user_phone')
        user = get_object_or_404(User, phone=user_phone)
        child = request.user  # Replace this line with your authentication mechanism
        UserChild.objects.create(user=user, child=child)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        child = request.user  # Replace this line with your authentication mechanism
        user_child = get_object_or_404(UserChild, user_id=user_id, child=child)
        user_child.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, user_child_id):
        state = request.data.get('state')
        user_child = get_object_or_404(UserChild, pk=user_child_id)
        user_child.state = state
        user_child.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        child = request.user  # Replace this line with your authentication mechanism
        user_childs = UserChild.objects.filter(user=child)
        data = [{'user_id': uc.user.id, 'user_name': uc.user.username} for uc in user_childs]
        return Response(data, status=status.HTTP_200_OK)