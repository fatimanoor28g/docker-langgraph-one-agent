"""The agent can use these two Python tools."""
from typing import Literal
from langchain_core.tools import tool
from .database import save_ticket

POLICIES = {
    "attendance": "Students need at least 75% attendance to sit exams.",
    "library": "Students may borrow 3 books for up to 14 days.",
    "fees": "Semester fees are due by the 10th day of the term.",
}


@tool
def get_policy(topic: Literal["attendance", "library", "fees"]) -> str:
    """Look up the university policy for attendance, library, or fees."""
    return POLICIES[topic]


@tool
def create_ticket(issue: str) -> str:
    """Create a university helpdesk complaint for a fictional student issue."""
    issue = issue.strip()
    if not issue:
        return "Please describe the problem before creating a ticket."
    ticket_id = save_ticket(issue)
    return f"Ticket #{ticket_id} created successfully (status: open)."
