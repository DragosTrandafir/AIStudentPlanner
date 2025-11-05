import os
from ai_system.agents.cs_agent import CSAgent
from dotenv import load_dotenv

# .env variables
load_dotenv()

# Tokens
hf_token = os.getenv("HF_TOKEN")

# model used by agents
agent_model = os.getenv("AGENT_MODEL")

cs_agent1 = CSAgent(hf_token, agent_model)
cs_agent1.propose_agent_plan("C:/Users/DragosTrandafiri/PycharmProjects/AlphaFlow/ai_system/agents/mock_data.json")
