from pydantic import BaseModel
from typing import Optional, Any


class Ticket(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    assignee: str
    description: str


class TicketDetail(Ticket):
    raw: Optional[Any]
