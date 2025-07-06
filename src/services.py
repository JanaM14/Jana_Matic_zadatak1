import httpx
from typing import List, Optional
from src.models import Ticket, TicketDetail


def priority(id: int) -> str:
    if id % 3 == 0:
        return "low"
    elif id % 3 == 1:
        return "medium"
    else:
        return "high"


def status(completed: bool) -> str:
    return "closed" if completed else "open"


async def fetch_todos() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/todos")
        response.raise_for_status()
        data = await response.json()
        return data


async def fetch_users() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/users")
        response.raise_for_status()
        data = await response.json()
        return data


async def fetch_tickets(
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
) -> List[Ticket]:
    todos = await fetch_todos()
    users = await fetch_users()

    user_map = {
        user.get("id"): (
            user.get("username").strip()
            if user.get("username", "").strip()
            else f'{user.get("firstName", "")} {user.get("lastName", "")}'.strip()
        )
        for user in users.get("users", [])
    }

    filtered = []

    for todo in todos.get("todos", []):
        tid = todo.get("id")
        if tid is None:
            continue

        t_status = status(todo.get("completed", False))
        t_priority = priority(tid)
        title = todo.get("todo") or ""
        user_id = todo.get("userId")

        if status_filter and t_status != status_filter:
            continue
        if priority_filter and t_priority != priority_filter:
            continue
        if q and q.lower() not in title.lower():
            continue

        assignee = user_map.get(user_id, "unknown")

        filtered.append(
            Ticket(
                id=tid,
                title=title,
                status=t_status,
                priority=t_priority,
                assignee=assignee,
                description=title[:100],
            )
        )

    return filtered[skip : skip + limit]


async def fetch_ticket_by_id(ticket_id: int) -> Optional[TicketDetail]:
    todos = await fetch_todos()
    users = await fetch_users()

    user_map = {
        user.get("id"): (
            user.get("username").strip()
            if user.get("username", "").strip()
            else f'{user.get("firstName", "")} {user.get("lastName", "")}'.strip()
        )
        for user in users.get("users", [])
    }

    for todo in todos.get("todos", []):
        if todo.get("id") == ticket_id:
            todo_id = todo.get("id")
            title = todo.get("todo") or ""
            user_id = todo.get("userId")
            completed = todo.get("completed", False)

            t_status = status(completed)
            t_priority = priority(todo_id)
            assignee = user_map.get(user_id, "unknown")

            return TicketDetail(
                id=todo_id,
                title=title,
                status=t_status,
                priority=t_priority,
                assignee=assignee,
                description=title[:100],
                raw=todo,
            )

    return None
