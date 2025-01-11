import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()

openaimodel = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'),model='gpt-4o-mini-2024-07-18')
