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
            session_id = serializer.data['session_id']
            agent = serializer.data['agent']
            response = ai_chatbot.get_llm_response(prompt, session_id, agent)

            return Response({"response": response})

class SessionID(APIView):
    def get(self, request):
        session_id = ai_chatbot.get_session_id()
        return Response({"session_id": session_id})



