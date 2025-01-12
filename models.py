import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()

from langchain_groq import ChatGroq

groqmodel = ChatGroq(
    model="llama3-70b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

openaimodel = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'),model='gpt-4o-mini-2024-07-18')


lmmodel = ChatOpenAI(
  model_name="qwen2.5-coder-7b-instruct",
  openai_api_base="https://eb17-2401-4900-1c21-2a82-7489-f6dd-1fd0-ad2b.ngrok-free.app/v1",
  openai_api_key="not-needed",
  temperature=0
)
