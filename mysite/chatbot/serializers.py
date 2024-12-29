from rest_framework import serializers

class AIResponseSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True)
    session_id = serializers.CharField(required=True)
    agent = serializers.CharField(required=False)

