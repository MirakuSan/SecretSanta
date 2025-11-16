from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Participant:
    name: str
    email: str


@dataclass
class Config:
    budget_limit: Optional[int]
    sender_name: str
    couples_exclusions: List[Tuple[str, str]]
