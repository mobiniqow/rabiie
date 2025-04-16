from logging import raiseExceptions

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from device.models import Relay10, Relay6, Psychrometer, Device
from device.serializers import Relay10Details, Relay6Details
from .models import Room, RoomDevice, RoomPicture
from .serializers import RoomSerializer, RoomDeviceSerializer, RoomPictureSerializer


class RoomView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(user=user)
class RoomDeviceListAPIView(APIView):
    def get(self, request, room_id):
        room_devices = RoomDevice.objects.filter(room_id=room_id)
        response_data = []

        for rd in room_devices:
            if rd.device:
                # بررسی Relay6
                relay6_fields = [f'device_r{i}' for i in range(1, 7)]
                for i, field in enumerate(relay6_fields, start=1):
                    relay = Relay6.objects.filter(**{field: rd.device}).first()
                    if relay:
                        response_data.append({
                            "type": "Device",
                            "device_id": str(rd.device.id),
                            "device_name": rd.device.name,
                            "device_image": rd.device.image.url if rd.device.image else None,
                            "connected_to": "Relay6",
                            "relay_id": str(relay.id),
                            "port_number": i,
                            "id":rd.id,
                            "port_name": getattr(relay, f'name{i}', ''),
                            "relay_state": getattr(relay, f'r{i}'),
                        })

                # بررسی Relay10
                relay10_fields = [f'device_r{i}' for i in range(1, 11)]
                for i, field in enumerate(relay10_fields, start=1):
                    relay = Relay10.objects.filter(**{field: rd.device}).first()
                    if relay:
                        response_data.append({
                            "type": "Device",
                            "device_id": str(rd.device.id),
                            "device_name": rd.device.name,
                            "device_image": rd.device.image.url if rd.device.image else None,
                            "connected_to": "Relay10",
                            "relay_id": str(relay.id),
                            "port_number": i,
                            "id":rd.id,
                            "port_name": getattr(relay, f'name{i}', ''),
                            "relay_state": getattr(relay, f'r{i}'),
                        })

            elif rd.psychrometer:
                for i in range(1, 7):
                    relay = Relay6.objects.filter(**{f't{i}': rd.psychrometer}).first()
                    if relay:
                        response_data.append({
                            "type": "Psychrometer",
                            "psychrometer_id": str(rd.psychrometer.id),
                            "psychrometer_name": rd.psychrometer.name,
                            "psychrometer_image": rd.psychrometer.image.image.url if rd.psychrometer.image and rd.psychrometer.image.image else None,
                            "connected_to": "Relay6",
                            "relay_id": str(relay.id),
                            "port_number": i,
                            "id": rd.id,
                            "port_name": getattr(relay, f'name{i}', ''),
                            "relay_state": getattr(relay, f'r{i}'),
                            "mode": rd.psychrometer.get_mod_display(),
                            "current_value": rd.psychrometer.current_value,
                            "destination_value": rd.psychrometer.destination_value,
                            "tolerance": rd.psychrometer.tolerance,
                        })

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, room_id):
        try:
            room_device = RoomDevice.objects.get(id=room_id)
        except RoomDevice.DoesNotExist:
            return Response({"detail": "RoomDevice not found."}, status=status.HTTP_404_NOT_FOUND)

        updated = False

        # Device Update
        if room_device.device:
            device = room_device.device
            if 'device_name' in request.data:
                device.name = request.data['device_name']
                updated = True
            if 'device_image' in request.FILES:
                device.image = request.FILES['device_image']
                updated = True
            device.save()

            # Relay port name and state update
            relay_models = [Relay6, Relay10]
            for relay_model in relay_models:
                for i in range(1, 11):  # max port number
                    field = f'device_r{i}'
                    try:
                        relay = relay_model.objects.get(**{field: device})
                        port_name_key = f'port_name_{i}'
                        relay_state_key = f'relay_state_{i}'

                        if port_name_key in request.data:
                            setattr(relay, f'name{i}', request.data[port_name_key])
                            updated = True
                        if relay_state_key in request.data:
                            setattr(relay, f'r{i}', request.data[relay_state_key])
                            updated = True

                        relay.save()
                    except relay_model.DoesNotExist:
                        continue

        # Psychrometer Update
        elif room_device.psychrometer:
            p = room_device.psychrometer
            psychro_fields = [
                'psychrometer_name', 'destination_value', 'tolerance',
                'hc', 'ma', 'on_of', 'plus_minus', 'current_value', 'mode'
            ]
            for field in psychro_fields:
                if field in request.data:
                    model_field = 'name' if field == 'psychrometer_name' else field
                    setattr(p, model_field, request.data[field])
                    updated = True

            if 'psychrometer_image' in request.FILES:
                if p.image:
                    p.image.image = request.FILES['psychrometer_image']
                else:
                    # اگر image قبلاً وجود نداشته باشه، یکی بساز
                    from device.models import Image
                    p.image = Image.objects.create(image=request.FILES['psychrometer_image'])
                updated = True

            # نام پورت و وضعیت در Relay6 برای Psychrometer
            for i in range(1, 7):
                try:
                    relay = Relay6.objects.get(**{f't{i}': p})
                    port_name_key = f'port_name_{i}'
                    relay_state_key = f'relay_state_{i}'
                    if port_name_key in request.data:
                        setattr(relay, f'name{i}', request.data[port_name_key])
                        updated = True
                    if relay_state_key in request.data:
                        setattr(relay, f'r{i}', request.data[relay_state_key])
                        updated = True
                    relay.save()
                except Relay6.DoesNotExist:
                    continue

            p.save()
            # ✅ Update port_name (RoomDevice field)
        if 'port_name' in request.data:
            room_device.port_name = request.data['port_name']
            room_device.save()
            updated = True

        else:
            return Response({"detail": "No device or psychrometer attached."}, status=status.HTTP_400_BAD_REQUEST)

        if updated:
            return Response({"detail": "Updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No fields updated."}, status=status.HTTP_400_BAD_REQUEST)


class RoomDeviceView(APIView):
    def get(self, request, room_id):
        user = request.user
        room_devices = RoomDevice.objects.filter(room__user=user, room_id=room_id)
        device_serializer = RoomDeviceSerializer(room_devices, many=True)
        device_ids = list(room_devices.values_list('device_id', flat=True))
        psychrometer_ids = list(room_devices.values_list('psychrometer', flat=True))
        device_ids += [pid for pid in psychrometer_ids if pid is not None]
        relay10_q = Q()
        for i in range(1, 11):
            relay10_q |= Q(**{f"device_r{i}__in": device_ids})
        relay6_q = Q()
        for i in range(1, 7):
            relay6_q |= Q(**{f"device_r{i}__in": device_ids})
            relay6_q |= Q(**{f"t{i}__in": device_ids})
        r10_devices = Relay10.objects.filter(user=user).filter(relay10_q)
        r6_devices = Relay6.objects.filter(user=user).filter(relay6_q)
        r10_serializer = Relay10Details(r10_devices, many=True)
        r6_serializer = Relay6Details(r6_devices, many=True)
        return Response({
            "room_devices": device_serializer.data,
            "relay10": r10_serializer.data,
            "relay6": r6_serializer.data,
            "device_ids":device_ids
        })

    def post(self, request, room_id):

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "اتاق مورد نظر پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoomDeviceSerializer(data=request.data)
        if serializer.is_valid(raiseExceptions=True):
            serializer.save(room=room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomPictureList(ListAPIView):
    serializer_class = RoomPictureSerializer
    queryset = RoomPicture.objects.all()
