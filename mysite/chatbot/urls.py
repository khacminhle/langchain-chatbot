from django.urls import path, include
from .views import AIChatBotView, SessionID

urlpatterns = [
    path('chatbot_response/', AIChatBotView.as_view()),
    path('get_session_id/', SessionID.as_view()),
]