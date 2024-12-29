import uuid

from .llm_models import get_openai_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages.ai import AIMessage



class AIChatBot:
    def __init__(self):
        self.llm = get_openai_model()
        self.system_template = """
        You're an intelligent person that excels in all areas of knowledge. 
        Answer the input below to the best of your knowledge.
        """

        self.chat_history = {}

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"{self.system_template}",
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
        )

        self.search_chat_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"{self.system_template}",
                ),
                ("placeholder", "{chat_history}"),
                MessagesPlaceholder(variable_name='agent_scratchpad'),
                ("human", "{input}"),
            ]
        )

        self.search_tools = [TavilySearchResults(max_results=10)]


    @staticmethod
    def get_session_id():
        return str(uuid.uuid4())

    def get_chat_history(self, session_id: str):

        if session_id not in self.chat_history:
            self.chat_history[session_id] = ChatMessageHistory()
        return self.chat_history[session_id]

    def get_llm_response(self, prompt: str, user_session_id: str, agent: str | None = None) -> str:
        if agent == "search_engine_agent":
            agent = create_tool_calling_agent(llm = self.llm, tools = self.search_tools, prompt=self.search_chat_prompt)
            agent_executor = AgentExecutor(agent=agent, tools=self.search_tools)

        else:
            # Use a different chat prompt without the agent scratch pad
            agent_executor = self.chat_prompt | self.llm

        chatbot_with_memory = RunnableWithMessageHistory(
            agent_executor,
            # pass the session into the get chat history and retrieve list of chat message
            lambda session_id: self.get_chat_history(session_id),
            input_messages_key =  "input",
            history_messages_key="chat_history",
        )

        response = chatbot_with_memory.invoke(
            {"input": prompt},
            {"configurable": {"session_id":user_session_id}},
        )

        # If there is a stuffs in agent scratch pad,
        # need to use 'output key' if there is no agent
        # action, it will be AI message, so check instance
        # for that

        if isinstance(response, AIMessage):
            return response.content
        else:
            return response["output"]






