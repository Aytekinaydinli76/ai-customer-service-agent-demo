from __future__ import annotations

import re
from dataclasses import dataclass

from .schemas import AgentResponse, Intent


@dataclass(frozen=True)
class IntentRule:
    intent: Intent
    terms: tuple[str, ...]
    reply: str
    next_action: str


RULES = (
    IntentRule(
        Intent.human_handoff,
        ("human", "person", "manager", "complaint", "urgent", "representative"),
        "I will connect you with a team member who can help.",
        "queue_human_handoff",
    ),
    IntentRule(
        Intent.cancel_appointment,
        ("cancel", "cancellation", "remove my appointment", "cannot come"),
        "I can help cancel the appointment after confirming its reference.",
        "request_appointment_reference",
    ),
    IntentRule(
        Intent.reschedule_appointment,
        ("reschedule", "change time", "change date", "move appointment", "another day"),
        "I can help find a new time for your existing appointment.",
        "request_appointment_reference",
    ),
    IntentRule(
        Intent.create_appointment,
        ("book", "booking", "appointment", "available", "availability", "schedule"),
        "I can help check availability and create an appointment.",
        "collect_service_and_date",
    ),
    IntentRule(
        Intent.business_question,
        ("price", "cost", "hours", "open", "location", "address", "service"),
        "I can answer that business question or connect you with the team.",
        "search_business_knowledge",
    ),
)


def normalize(message: str) -> str:
    return re.sub(r"\s+", " ", message.lower()).strip()


def classify(message: str) -> AgentResponse:
    normalized = normalize(message)
    best_rule: IntentRule | None = None
    best_matches: list[str] = []

    for rule in RULES:
        matches = [term for term in rule.terms if term in normalized]
        if len(matches) > len(best_matches):
            best_rule = rule
            best_matches = matches

    if best_rule is None:
        return AgentResponse(
            intent=Intent.unknown,
            confidence=0.25,
            reply="I am not fully sure what you need. Would you like a team member to help?",
            requires_human=True,
            next_action="ask_clarifying_question",
            matched_terms=[],
        )

    confidence = min(0.95, 0.58 + (0.12 * len(best_matches)))
    return AgentResponse(
        intent=best_rule.intent,
        confidence=round(confidence, 2),
        reply=best_rule.reply,
        requires_human=best_rule.intent == Intent.human_handoff,
        next_action=best_rule.next_action,
        matched_terms=best_matches,
    )
