from src.core.state import AgentState
from src.agents.analyst import AnalystAgent
from src.agents.strategist import StrategistAgent
from src.agents.publisher import PublisherAgent # <--- Import the new class

def analyst_node(state: AgentState):
    agent = AnalystAgent()
    return agent.run(state)

def strategist_node(state: AgentState):
    agent = StrategistAgent()
    return agent.run(state)

def publisher_node(state: AgentState):
    agent = PublisherAgent()
    return agent.run(state)