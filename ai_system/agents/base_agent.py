class BaseAgent:
    def __init__(self, token, model):
        self.token = token
        self.model = model

    def propose_agent_plan(self,subject_data):
        raise NotImplementedError

