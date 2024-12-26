from rest_framework import serializers

class AIResponseSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True)

