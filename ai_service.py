import json
import os
import re
from typing import Any, Dict, List

import httpx


DO_INFERENCE_URL = "https://inference.do-ai.run/v1/chat/completions"
DEFAULT_MODEL = os.getenv("DO_INFERENCE_MODEL", "anthropic-claude-4.6-sonnet")


def _extract_json(text: str) -> str:
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


def _coerce_unstructured_payload(raw_text: str) -> dict[str, object]:
    compact = raw_text.strip()
    normalized = compact.replace("\n", ",")
    tags = [part.strip(" -•\t") for part in normalized.split(",") if part.strip(" -•\t")]
    if not tags:
        tags = ["guided plan", "saved output", "shareable insight"]
    headline = tags[0].title()
    items = []
    for index, tag in enumerate(tags[:3], start=1):
        items.append({
            "title": f"Stage {index}: {tag.title()}",
            "detail": f"Use {tag} to move the request toward a demo-ready outcome.",
            "score": min(96, 80 + index * 4),
        })
    highlights = [tag.title() for tag in tags[:3]]
    return {
        "note": "Model returned plain text instead of JSON",
        "raw": compact,
        "text": compact,
        "summary": compact or f"{headline} fallback is ready for review.",
        "tags": tags[:6],
        "items": items,
        "score": 88,
        "insights": [f"Lead with {headline} on the first screen.", "Keep one clear action visible throughout the flow."],
        "next_actions": ["Review the generated plan.", "Save the strongest output for the demo finale."],
        "highlights": highlights,
    }

def _normalize_inference_payload(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        return _coerce_unstructured_payload(str(payload))
    normalized = dict(payload)
    summary = str(normalized.get("summary") or normalized.get("note") or "AI-generated plan ready")
    raw_items = normalized.get("items")
    items: list[dict[str, object]] = []
    if isinstance(raw_items, list):
        for index, entry in enumerate(raw_items[:3], start=1):
            if isinstance(entry, dict):
                title = str(entry.get("title") or f"Stage {index}")
                detail = str(entry.get("detail") or entry.get("description") or title)
                score = float(entry.get("score") or min(96, 80 + index * 4))
            else:
                label = str(entry).strip() or f"Stage {index}"
                title = f"Stage {index}: {label.title()}"
                detail = f"Use {label} to move the request toward a demo-ready outcome."
                score = float(min(96, 80 + index * 4))
            items.append({"title": title, "detail": detail, "score": score})
    if not items:
        items = _coerce_unstructured_payload(summary).get("items", [])
    raw_insights = normalized.get("insights")
    if isinstance(raw_insights, list):
        insights = [str(entry) for entry in raw_insights if str(entry).strip()]
    elif isinstance(raw_insights, str) and raw_insights.strip():
        insights = [raw_insights.strip()]
    else:
        insights = []
    next_actions = normalized.get("next_actions")
    if isinstance(next_actions, list):
        next_actions = [str(entry) for entry in next_actions if str(entry).strip()]
    else:
        next_actions = []
    highlights = normalized.get("highlights")
    if isinstance(highlights, list):
        highlights = [str(entry) for entry in highlights if str(entry).strip()]
    else:
        highlights = []
    if not insights and not next_actions and not highlights:
        fallback = _coerce_unstructured_payload(summary)
        insights = fallback.get("insights", [])
        next_actions = fallback.get("next_actions", [])
        highlights = fallback.get("highlights", [])
    return {
        **normalized,
        "summary": summary,
        "items": items,
        "score": float(normalized.get("score") or 88),
        "insights": insights,
        "next_actions": next_actions,
        "highlights": highlights,
    }


async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    api_key = os.getenv("GRADIENT_MODEL_ACCESS_KEY") or os.getenv("DIGITALOCEAN_INFERENCE_KEY")
    if not api_key:
        return {
            "ok": False,
            "note": "AI temporarily unavailable: missing inference key.",
            "data": {},
        }

    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_completion_tokens": 512 if max_tokens < 256 else max_tokens,
        "temperature": 0.5,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(DO_INFERENCE_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

        content = ""
        choices = result.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            content = message.get("content", "")

        cleaned = _extract_json(content)
        parsed = json.loads(cleaned)
        return {"ok": True, "note": "", "data": parsed}
    except Exception as exc:
        return {
            "ok": False,
            "note": f"AI temporarily unavailable. Using fallback output. Details: {str(exc)}",
            "data": {},
        }


async def generate_brief_payload(query: str, preferences: str) -> Dict[str, Any]:
    system = (
        "You are a product planning workbench engine. Return strict JSON only with keys: "
        "summary (string), items (array of objects), score (number), traceability (array), "
        "resolution_notes (array), clarification_cards (array)."
    )
    user = (
        "Generate a structured planning brief from rough notes. "
        f"Notes: {query}\nPreferences: {preferences}\n"
        "Each item should be {section, content, source_phrases}."
    )

    response = await _call_inference(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=512,
    )

    if response["ok"] and response["data"]:
        return response["data"]

    fallback_items = [
        {
            "section": "Problem Statement",
            "content": "Users have rough product notes but no clear structure to act on.",
            "source_phrases": ["rough notes", "clear way to act", "blank product spec"],
        },
        {
            "section": "Target User Profile",
            "content": "Founders, indie makers, PMs, students, and innovation teams with incomplete context.",
            "source_phrases": ["incomplete context", "product planning"],
        },
        {
            "section": "Feature Stack",
            "content": "Traceable brief generation, clarification cards, and snapshot pinboard.",
            "source_phrases": ["traceable", "clarification", "snapshot"],
        },
    ]
    return {
        "summary": "Structured first-pass brief generated with fallback planner.",
        "items": fallback_items,
        "score": 78,
        "traceability": [
            {"section": "Problem Statement", "mapped_phrase": "blank product spec"},
            {"section": "Feature Stack", "mapped_phrase": "saved artifacts"},
        ],
        "resolution_notes": [
            "Assumed MVP focus because timeline detail was not explicit.",
            "Left monetization open due to missing pricing assumptions.",
        ],
        "clarification_cards": [
            "Who is the primary user segment for v1?",
            "What success metric defines a good first release?",
            "What constraints matter most: budget, team size, or timeline?",
        ],
        "note": response.get("note", "AI temporarily unavailable."),
    }


async def generate_insights_payload(selection: str, context: str) -> Dict[str, Any]:
    system = (
        "You are a product planning analyst. Return strict JSON with keys: "
        "insights (array of strings), next_actions (array of strings), highlights (array of strings)."
    )
    user = (
        f"Selection: {selection}\nContext: {context}\n"
        "Generate practical planning insights tied to ambiguity resolution and iteration steps."
    )

    response = await _call_inference(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=512,
    )

    if response["ok"] and response["data"]:
        return response["data"]

    return {
        "insights": [
            "Your selected section is strongest when tied to one explicit success metric.",
            "The brief implies two audiences; narrowing to one persona will improve scope decisions.",
        ],
        "next_actions": [
            "Pick one primary user persona for MVP.",
            "Define one measurable success criterion for the first 30 days.",
            "Cut one non-critical feature from v1 scope.",
        ],
        "highlights": [
            "Ambiguity detected in target users.",
            "Scope conflict between speed and feature depth.",
        ],
        "note": response.get("note", "AI temporarily unavailable."),
    }
