from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_openai_model() -> ChatOpenAI:
    model = ChatOpenAI()
    return model

