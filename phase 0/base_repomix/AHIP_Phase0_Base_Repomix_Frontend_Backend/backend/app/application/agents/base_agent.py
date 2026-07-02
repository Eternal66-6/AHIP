from abc import ABC, abstractmethod
from app.domain.schemas.schemas import AgentOutput

class BaseHealthcareAgent(ABC):
    agent_name: str

    @abstractmethod
    def run(self, case_id: str, context: dict) -> AgentOutput:
        raise NotImplementedError
