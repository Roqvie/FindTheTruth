from rest_framework import serializers


class PhotoSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    photo_url = serializers.ImageField()


class AnswerSerializer(serializers.Serializer):

    is_real = serializers.BooleanField()