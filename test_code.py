from mysite.chatbot.ai_components.ai_chatbot import AIChatBot

chatbot = AIChatBot()

print(chatbot.get_session_id())
while True:
    prompt = input("> ")
    response = chatbot.get_llm_response(prompt)
    print(response)
