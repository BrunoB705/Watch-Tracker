from dataclasses import dataclass
from typing import Optional

@dataclass
class Media:
    id: Optional[int] = None
    title: str = ""
    url: str = ""
    current_seconds: int = 0
    status: str = "pending"  # 'pending' o 'completed'
    created_at: Optional[str] = None
    updated_at: Optional[str] = None