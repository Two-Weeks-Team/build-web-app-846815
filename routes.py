import json
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ai_service import generate_brief_payload, generate_insights_payload
from models import SessionLocal, SeedPrompt, WorkbenchProject, PlanningSnapshot


router = APIRouter()


class PlanRequest(BaseModel):
    query: str
    preferences: Optional[str] = ""


class InsightRequest(BaseModel):
    selection: str
    context: str


class SaveSnapshotRequest(BaseModel):
    title: str
    query: str
    preferences: Optional[str] = ""
    summary: str
    items: List[dict]
    change_summary: Optional[str] = "Initial snapshot"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/plan")
@router.post("/plan")
async def create_plan(payload: PlanRequest, db: Session = Depends(get_db)):
    brief = await generate_brief_payload(payload.query, payload.preferences or "")

    project = WorkbenchProject(
        title="Auto Draft " + datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        raw_notes=payload.query,
        preferences=payload.preferences or "",
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "summary": brief.get("summary", "Generated plan."),
        "items": brief.get("items", []),
        "score": brief.get("score", 70),
        "traceability": brief.get("traceability", []),
        "resolution_notes": brief.get("resolution_notes", []),
        "clarification_cards": brief.get("clarification_cards", []),
        "project_id": project.id,
        "note": brief.get("note", ""),
    }


@router.post("/insights")
@router.post("/insights")
async def create_insights(payload: InsightRequest):
    data = await generate_insights_payload(payload.selection, payload.context)
    return {
        "insights": data.get("insights", []),
        "next_actions": data.get("next_actions", []),
        "highlights": data.get("highlights", []),
        "note": data.get("note", ""),
    }


@router.get("/seed-prompts")
@router.get("/seed-prompts")
def list_seed_prompts(db: Session = Depends(get_db)):
    rows = db.query(SeedPrompt).order_by(SeedPrompt.id.asc()).all()
    return {
        "items": [
            {"id": r.id, "name": r.name, "notes": r.notes} for r in rows
        ]
    }


@router.post("/snapshots")
@router.post("/snapshots")
def save_snapshot(payload: SaveSnapshotRequest, db: Session = Depends(get_db)):
    project = WorkbenchProject(
        title=payload.title,
        raw_notes=payload.query,
        preferences=payload.preferences or "",
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    snapshot = PlanningSnapshot(
        project_id=project.id,
        title=payload.title,
        summary=payload.summary,
        brief_json=json.dumps(payload.items),
        change_summary=payload.change_summary or "Initial snapshot",
        thumbnail_text=(payload.summary[:120] + "...") if len(payload.summary) > 120 else payload.summary,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return {
        "id": snapshot.id,
        "project_id": project.id,
        "title": snapshot.title,
        "summary": snapshot.summary,
        "created_at": snapshot.created_at.isoformat(),
        "thumbnail_text": snapshot.thumbnail_text,
    }


@router.get("/snapshots")
@router.get("/snapshots")
def list_snapshots(db: Session = Depends(get_db)):
    rows = db.query(PlanningSnapshot).order_by(PlanningSnapshot.created_at.desc()).limit(20).all()
    return {
        "items": [
            {
                "id": r.id,
                "project_id": r.project_id,
                "title": r.title,
                "summary": r.summary,
                "change_summary": r.change_summary,
                "thumbnail_text": r.thumbnail_text,
                "created_at": r.created_at.isoformat(),
            }
            for r in rows
        ]
    }


@router.get("/snapshots/{snapshot_id}")
@router.get("/snapshots/{snapshot_id}")
def get_snapshot(snapshot_id: int, db: Session = Depends(get_db)):
    row = db.query(PlanningSnapshot).filter(PlanningSnapshot.id == snapshot_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return {
        "id": row.id,
        "project_id": row.project_id,
        "title": row.title,
        "summary": row.summary,
        "items": json.loads(row.brief_json),
        "change_summary": row.change_summary,
        "thumbnail_text": row.thumbnail_text,
        "created_at": row.created_at.isoformat(),
    }
