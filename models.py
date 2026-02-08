from pydantic import BaseModel
from typing import List, Dict, Any

class Lead(BaseModel):
    lead_id: str
    company: Dict[str, Any]
    signal: Dict[str, Any]
    products: List[Dict[str, Any]]
    score: Dict[str, Any]
    routing: Dict[str, Any]
    created_at: str
