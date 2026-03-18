from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from models import Base, SessionLocal, SeedPrompt, engine
from routes import router


app = FastAPI(title="Build Web App API", version="1.0.0")


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        count = db.query(SeedPrompt).count()
        if count == 0:
            seeds = [
                SeedPrompt(name="Build Web App", notes="A rough opportunity note about a 12-year-old app developer wanting a usable planning workflow."),
                SeedPrompt(name="Campus Club Scheduler", notes="Scattered notes about events, member reminders, and role permissions."),
                SeedPrompt(name="Neighborhood Swap Board", notes="A messy concept for borrowing tools and coordinating pickups."),
                SeedPrompt(name="Creator Lesson Builder", notes="An incomplete idea about turning expertise into guided mini-courses."),
                SeedPrompt(name="Pet Care Routine Planner", notes="Fragmented requirements for shared feeding, meds, and caretaker notes."),
            ]
            db.add_all(seeds)
            db.commit()
    finally:
        db.close()



@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def root():
    html = """
    <html>
      <head>
        <title>Build Web App API</title>
        <style>
          body { font-family: Inter, Arial, sans-serif; background: #0b1020; color: #e6edf7; margin: 0; padding: 24px; }
          .card { background: #141b2d; border: 1px solid #28324a; border-radius: 12px; padding: 18px; margin-bottom: 16px; }
          h1 { margin: 0 0 10px 0; color: #f8d66d; }
          a { color: #86b7ff; text-decoration: none; }
          code { color: #a9d1ff; }
          ul { line-height: 1.7; }
        </style>
      </head>
      <body>
        <div class='card'>
          <h1>Build Web App API</h1>
          <p>Turn rough product notes into a structured, traceable brief you can refine and save in minutes.</p>
        </div>
        <div class='card'>
          <h2>Endpoints</h2>
          <ul>
            <li><code>GET /health</code></li>
            <li><code>POST /plan</code> and <code>POST /api/plan</code></li>
            <li><code>POST /insights</code> and <code>POST /api/insights</code></li>
            <li><code>GET /seed-prompts</code> and <code>GET /api/seed-prompts</code></li>
            <li><code>POST /snapshots</code> and <code>POST /api/snapshots</code></li>
            <li><code>GET /snapshots</code> and <code>GET /api/snapshots</code></li>
            <li><code>GET /snapshots/{snapshot_id}</code> and <code>GET /api/snapshots/{snapshot_id}</code></li>
          </ul>
        </div>
        <div class='card'>
          <h2>Tech Stack</h2>
          <p>FastAPI 0.115.0 · SQLAlchemy 2.0.35 · Pydantic 2.9.0 · PostgreSQL/SQLite · DO Serverless Inference (anthropic-claude-4.6-sonnet)</p>
          <p><a href='/docs'>Swagger Docs</a> · <a href='/redoc'>ReDoc</a></p>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
