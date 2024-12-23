from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .ai_components.ai_chatbot import AIChatBot
from .serializers import AIResponseSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
ai_chatbot = AIChatBot()


class AIChatBotView(APIView):
    """
    This view handles the main interaction with the AI chatbot.
    It receives a prompt and returns an AI-generated answer.
    """
    @swagger_auto_schema(request_body=AIResponseSerializer)
    def post(self, request):
        serializer = AIResponseSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.data['prompt']
            response = ai_chatbot.get_llm_response(prompt)
            return Response(response)



