from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from device.models import Relay12, Relay6
from device.serializers import Relay12Serializer, Relay6Serializer


@api_view(("GET", "PATCH"))
def search_device(request, product_id):
    if request.method == 'GET':
        devices = Relay12.objects.filter(product_id=product_id)

        if not devices.exists():
            devices = Relay6.objects.filter(product_id=product_id)

        if not devices.exists():
            return Response({"message": "device not found"},
                            status=status.HTTP_404_NOT_FOUND)

        device = devices.first()
        device.reset()
        device.user = request.user
        device.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PATCH':
        devices = Relay12.objects.filter(product_id=product_id)
        if devices.exists():
            serializer = Relay12Serializer(devices.first(), data=request.data, partial=True)
        if not devices.exists():
            devices = Relay6.objects.filter(product_id=product_id)
            if devices.exists():
                serializer = Relay6Serializer(devices.first(), data=request.data, partial=True)
        if not devices.exists():
            return Response({"message": "object not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data})


class DeviceViewSet(APIView):
    def get(self, request, ):
        r12_devices = Relay12.objects.filter(user=request.user)
        r6_devices = Relay6.objects.filter(user=request.user)
        r12_serializer = Relay12Serializer(r12_devices, many=True)
        r6_serializer = Relay6Serializer(r6_devices, many=True)
        return Response(
            {
                "r12": r12_serializer.data,
                "r6": r6_serializer.data
            })
