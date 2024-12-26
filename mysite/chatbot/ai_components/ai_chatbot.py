import uuid

from .llm_models import get_openai_model
from langchain_core.prompts import ChatPromptTemplate



class AIChatBot:
    def __init__(self):
        self.llm = get_openai_model()
        self.system_template = """
        You're an intelligent person that excels in all areas of knowledge. 
        Answer the question below to the best of your knowledge.
        {question}
        """
    @staticmethod
    def get_session_id():
        return str(uuid.uuid4())

    def get_llm_response(self, prompt):

        prompt_template = ChatPromptTemplate.from_template(self.system_template)
        chain = prompt_template | self.llm
        response = chain.invoke({"question": prompt})
        return response.content




