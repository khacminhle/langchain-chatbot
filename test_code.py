from mysite.chatbot.ai_components.ai_chatbot import AIChatBot

chatbot = AIChatBot()

session_id = chatbot.get_session_id()

print(session_id)

while True:
    prompt = input("> ")
    response = chatbot.get_llm_response(prompt, session_id)
    print(response)


