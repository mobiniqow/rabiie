from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .permissions import UserPermission
from .serializers import UserSerializers, UserSerializer2
from .utils import getRandomGenerator, sendMessage, get_or_default
from .validations import isValidPhoneNumber
from rest_framework import viewsets
from .terms import terms


class VerifyUser(APIView):
    def post(self, request):
        try:
            phone = request.data['phone']
            password = request.data['code']
            old_user = User.objects.filter(phone=phone)
            if old_user.exists():
                old_user = old_user[0]
                if old_user.check_password(password):
                    old_user.is_active = True
                    old_user.save()
                    refresh = RefreshToken.for_user(old_user)
                    return Response({'token': str(refresh.access_token)})
                else:
                    return Response({"message": "wrong password"}, status=400)
            else:
                return Response({"message": "user not exists"}, status=400)
        except Exception as e:
            return Response({"message": str(e)}, status=400)


class LoginUser(APIView):
    def post(self, request):
        try:
            phone = request.data['phone']
            if isValidPhoneNumber(phone):
                old_user = User.objects.filter(phone=phone)
                if old_user.exists():
                    old_user = old_user[0]
                    _password = User.objects.make_random_password(allowed_chars='123456789', length=4)
                    _password = "1111"
                    sendMessage(phone, _password)
                    old_user.set_password(_password)
                    old_user.save()
                    return Response({"message": "opt code sending"})
                else:
                    _password = User.objects.make_random_password(allowed_chars='123456789', length=4)
                    _password = "1111"
                    new_user = User(phone=phone)
                    new_user.role = User.Role.USER
                    new_user.set_password(_password)
                    sendMessage(phone, _password)
                    new_user.save()
                    return Response({"message": "new opt code sending"})
            else:
                return Response({"message": "invalid phone number"}, status=400)
        except Exception as e:

            return Response({"message": str(e)}, status=400)


class UserProfile(APIView):
    permission_classes = [UserPermission]

    def post(self, request):
        try:
            user = request.user
            first_name = get_or_default(request, 'first_name', user.first_name)
            last_name = get_or_default(request, 'last_name', user.last_name)
            request.user.first_name = first_name
            request.user.last_name = last_name
            # request.user.avatar = avatar
            request.user.save()
            return Response({"message": 'profile updated'})
        except Exception as e:
            return Response({"message": f'{e}'}, status=400)

    def get(self, request):
        try:
            serializer = UserSerializers(request.user)

            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f'{e}'}, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer2


@api_view(("POST",))
def get_user_by_national_id(request):
    if request.method == "POST":
        try:
            national_id = request.POST['nationalId']
            user = User.objects.filter(national_id=national_id)[0]
            serializer = UserSerializer2(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': 'user not exist'}, 400)


@api_view(("GET",))
def get_access(request):
    if request.method == "GET":
        try:
            return Response({"role": request.user.role, "details": UserSerializers(request.user).data})
        except Exception as e:
            return Response(str(e))


@api_view(('GET',))
def terms_and_conditions(request):
    return Response({'message': terms})
