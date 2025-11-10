import os
from ai_system.agents.cs_agent import CSAgent
from dotenv import load_dotenv

from ai_system.agents.math_agent import MathAgent

# .env variables
load_dotenv()

# Tokens
hf_token = os.getenv("HF_TOKEN")

# model used by agents
custom_agent_model = os.getenv("CUSTOM_AGENT_MODEL")

# (consider current date)

# cs_agent1 = CSAgent(hf_token, custom_agent_model)
# response = cs_agent1.propose_agent_plan("C:/Users/DragosTrandafiri/PycharmProjects/AlphaFlow/ai_system/agents"
#                                         "/mock_data_cs.json")
# print(response)
#
cs_agent2 = MathAgent(hf_token, custom_agent_model)
response = cs_agent2.propose_agent_plan("C:/Users/DragosTrandafiri/PycharmProjects/AlphaFlow/ai_system/agents"
                                        "/mock_data_math.json")
print(response)

# cs_agent3 = MathAgent(hf_token, custom_agent_model)
# response = cs_agent3.propose_agent_plan("C:/Users/DragosTrandafiri/PycharmProjects/AlphaFlow/ai_system/agents"
#                                         "/mock_data_math_easy.json")
# print(response)