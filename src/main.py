from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from enum import Enum
import traceback

from src.models import Ticket, TicketDetail
from src.services import fetch_tickets, fetch_ticket_by_id


app = FastAPI()


@app.get("/pin")
async def pin():
    return {"message": "pin "}


class StatusEnum(str, Enum):
    open = "open"
    closed = "closed"


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


@app.get("/tickets", response_model=List[Ticket])
async def get_tickets(
    status: Optional[StatusEnum] = Query(None),
    priority: Optional[PriorityEnum] = Query(None),
    q: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    tickets = await fetch_tickets(
        status_filter=status.value if status else None,
        priority_filter=priority.value if priority else None,
        q=q,
        skip=skip,
        limit=limit,
    )
    return tickets


@app.get("/tickets/{ticket_id}", response_model=TicketDetail)
async def get_ticket_by_id(ticket_id: int):
    ticket = await fetch_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.get("/tickets/search", response_model=List[Ticket])
async def search_tickets(
    q: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    return await fetch_tickets(q=q, skip=skip, limit=limit)


@app.get("/stats")
async def get_stats():
    tickets = await fetch_tickets(limit=1000)

    from collections import Counter

    status_count = Counter(t.status for t in tickets)
    priority_count = Counter(t.priority for t in tickets)

    return {"status_counts": status_count, "priority_counts": priority_count}


@app.get("/health")
async def health():
    return {"status": "ok"}
