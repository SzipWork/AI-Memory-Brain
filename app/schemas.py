from pydantic import BaseModel, Field
from datetime import datetime

class Memory(BaseModel):
    content: str
    confidence: float = 0.6
    importance: float = 0.5
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
