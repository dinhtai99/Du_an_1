from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.schemas.script import ScriptGenerateRequest, StructuredScriptOutput

class LLMProvider(ABC):
    @abstractmethod
    async def generate_script(
        self,
        request: ScriptGenerateRequest,
        cultural_knowledge: str
    ) -> StructuredScriptOutput:
        """Generate structured script validated by Pydantic"""
        pass

    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """Check provider connectivity and status"""
        pass
