from django.urls import path, include
from .views import AIChatBotView

urlpatterns = [
    path('chatbot_response/', AIChatBotView.as_view()),
]