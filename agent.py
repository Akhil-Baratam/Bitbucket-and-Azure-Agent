from dotenv import load_dotenv
load_dotenv()
from tools import manage_repo_and_get_file, commit_changes_and_raise_pr
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from prompts import bitbucket_prompt
from models import openaimodel

class aiAgent:
  def __init__(self, tools, prompts, model):
    self.tools = tools
    self.prompts = prompts
    self.model = model
    self.prompt = ''

  def run_agent(self):
    self.prompt = ChatPromptTemplate([
      ("system",self.prompts['system']),
      ("human","{input}"),
      ("placeholder", "{agent_scratchpad}")
    ])
    agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
    agent_executer = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    response = agent_executer.invoke({"input":self.prompts['human']})
    return response
  
if __name__ == '__main__':
  tools = [manage_repo_and_get_file, commit_changes_and_raise_pr]

  agent = aiAgent(tools, bitbucket_prompt, openaimodel)
  response = agent.run_agent()
  print(response)