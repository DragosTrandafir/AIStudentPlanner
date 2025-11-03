class BaseAgent:
    def __init__(self, name, model):
        self.name = name
        self.model = model

    def propose_agent_plan(self):
        raise NotImplementedError

