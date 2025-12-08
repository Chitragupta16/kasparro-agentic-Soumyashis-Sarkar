# src/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """
    Abstract Base Class for all agents in the system.
    Enforces a strict contract: every agent must implement execute().
    """
    
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        The single responsibility method.
        Input: Structured data (Model or Dict)
        Output: Structured data (Model or Dict)
        """
        pass

    def log(self, message: str):
        """Standardized internal logging."""
        print(f"[{self.name}] {message}")