import uuid

from .llm_models import get_openai_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory



class AIChatBot:
    def __init__(self):
        self.llm = get_openai_model()
        self.system_template = """
        You're an intelligent person that excels in all areas of knowledge. 
        Answer the input below to the best of your knowledge.
        """

        self.chat_history = {}

    def get_chat_history(self, session_id: str):

        if session_id not in self.chat_history:
            self.chat_history[session_id] = ChatMessageHistory()
        return self.chat_history[session_id]

    @staticmethod
    def get_session_id():
        return str(uuid.uuid4())

    def get_llm_response(self, prompt: str, user_session_id: str) -> str:

        # prompt_template = ChatPromptTemplate.from_template(self.system_template)
        # chain = prompt_template | self.llm
        # response = chain.invoke({"input": prompt})
        # return response.content

        chat_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"{self.system_template}",
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
        )
        chain = chat_prompt | self.llm

        chatbot_with_memory = RunnableWithMessageHistory(
            chain,
            # pass the session into the get chat history and retrieve list of chat message
            lambda session_id: self.get_chat_history(session_id),
            input_messages_key =  "input",
            history_messages_key="chat_history",
        )

        response = chatbot_with_memory.invoke(
            {"input": prompt},
            {"configurable": {"session_id":user_session_id}},
        )

        return response.content







