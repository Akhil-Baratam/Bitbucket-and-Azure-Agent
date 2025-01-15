from dotenv import load_dotenv
load_dotenv()
from tools import manage_repo_and_get_file, commit_changes_and_raise_pr
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from prompts import bitbucket_prompt
from models import openaimodel, lmmodel, groqmodel
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for all origins (you can restrict this to specific origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str
    selected_target: str

class aiAgent:
    def __init__(self, tools, prompts, model):
        self.tools = tools
        self.prompts = prompts
        self.model = model
        self.prompt = ''

    def run_agent(self, human_prompt):
        try:
            self.prompts['human'] = human_prompt
            self.prompt = ChatPromptTemplate([
                ("system", self.prompts['system']),
                ("human", self.prompts['human']),
                ("placeholder", "{agent_scratchpad}")
            ])
            agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
            agent_executer = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
            response = agent_executer.invoke({"input": self.prompts['human']})
            return response
        except Exception as e:
            print(f"Error occurred in aiAgent.run_agent: {e}")
            raise

@app.post("/run-agent/")
async def run_agent(prompt_request: PromptRequest):
    tools = [manage_repo_and_get_file, commit_changes_and_raise_pr]
    try:
        # Print the incoming payload for debugging
        print(f"Received payload: {prompt_request.json()}")  # Print the JSON payload

        agent = aiAgent(tools, bitbucket_prompt, openaimodel)
        human_prompt = f"{prompt_request.prompt}\nrepo_slug: {prompt_request.selected_target}\n repo_path: ./{prompt_request.selected_target}\n workspace: sampleforbbagent"
        response = agent.run_agent(human_prompt)
        return {"response": response}
    except Exception as e:
        print(f"Error occurred while running the agent: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == '__main__':
    tools = [manage_repo_and_get_file, commit_changes_and_raise_pr]
    agent = aiAgent(tools, bitbucket_prompt, openaimodel)
    response = agent.run_agent()
    print(response)
