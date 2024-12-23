from mysite.chatbot import AIChatBot

chatbot = AIChatBot()

while True:
    prompt = input("> ")
    response = chatbot.get_llm_response(prompt)
    print(response)
