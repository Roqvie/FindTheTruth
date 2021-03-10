from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from .models import Photo
from .serializers import PhotoSerializer, AnswerSerializer


class PhotoView(APIView):
    """View to get photos from API"""

    def get(self, request, type, h, w):
        """GET method"""
        if h <= 4 and w <= 4 and h*w >= 2:
            real_photos = Photo.objects.order_by("?").filter(is_real=True, type=type)[:1]
            fake_photos = Photo.objects.order_by("?").filter(is_real=False, type=type)[:h*w-1]
            photos = real_photos | fake_photos
            serializer = PhotoSerializer(photos.order_by("?"), many=True)
            return Response(serializer.data)
        else:
            res = {"code": 400, "error": "App only provides 1*1 to 4*4 grid"}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)


class GuesserView(APIView):
    """View to get photo info from API"""

    def get(self, request, pk):
        """GET method"""
        try:
            photo = Photo.objects.get(id=pk)
            serializer = AnswerSerializer(photo)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            res = {"code": 400, "error": "Photo does not exist"}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)