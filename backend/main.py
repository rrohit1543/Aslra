"""
FastAPI application for the ArSL Transcriber.
Serves API endpoints and static frontend files.
"""
from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    TranscribeRequest,
    TranscribeResponse,
    RuleListResponse,
    SourceListResponse,
    DictionaryListResponse,
    HealthResponse,
    GrammarRule,
)
from .rules_loader import load_rules, get_rule_by_id
from .sources import load_sources, get_source_by_id
from .dictionary import SignDictionary
from .analyzer import analyze
from .engine import TranscriptionEngine


# ─── App setup ────────────────────────────────────────────────────

app = FastAPI(
    title="ArSL Transcriber",
    description="Arabic Sign Language Grammar Discovery & Explainable Transcription Prototype",
    version="0.1.0",
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Data loading (startup) ──────────────────────────────────────

rules_data: list[GrammarRule] = []
sources_data = []
dictionary = SignDictionary()
engine: TranscriptionEngine | None = None


@app.on_event("startup")
async def startup_load_data():
    """Load all data files at startup."""
    global rules_data, sources_data, dictionary, engine

    print("[ArSL Transcriber] Loading data files...")
    rules_data = load_rules()
    sources_data = load_sources()
    dictionary.load()

    engine = TranscriptionEngine(
        rules=rules_data,
        dictionary=dictionary,
        sources=sources_data,
    )

    print(f"[ArSL Transcriber] Ready — {len(rules_data)} rules, {len(sources_data)} sources, {len(dictionary.entries)} dictionary entries")


# ─── API Routes ───────────────────────────────────────────────────

@app.get("/api/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        rules_loaded=len(rules_data),
        sources_loaded=len(sources_data),
        dictionary_loaded=len(dictionary.entries),
    )


@app.post("/api/transcribe", response_model=TranscribeResponse)
async def transcribe(request: TranscribeRequest):
    """Transcribe an Arabic sentence into ArSL gloss sequence with full explanation."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    # Analyze the input
    analysis = analyze(request.text)

    # Run through the transcription engine
    result = engine.transcribe(analysis)

    return result


@app.get("/api/rules", response_model=RuleListResponse)
async def list_rules():
    """List all grammar rules with evidence and confidence."""
    return RuleListResponse(
        count=len(rules_data),
        rules=rules_data,
    )


@app.get("/api/rules/{rule_id}")
async def get_rule(rule_id: str):
    """Get a single rule by ID."""
    rule = get_rule_by_id(rules_data, rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail=f"Rule {rule_id} not found")
    return rule


@app.get("/api/sources", response_model=SourceListResponse)
async def list_sources():
    """List all sources."""
    return SourceListResponse(
        count=len(sources_data),
        sources=sources_data,
    )


@app.get("/api/sources/{source_id}")
async def get_source(source_id: str):
    """Get a single source by ID."""
    source = get_source_by_id(sources_data, source_id)
    if source is None:
        raise HTTPException(status_code=404, detail=f"Source {source_id} not found")
    return source


@app.get("/api/dictionary", response_model=DictionaryListResponse)
async def list_dictionary():
    """List all dictionary entries."""
    entries = dictionary.get_all_entries()
    return DictionaryListResponse(
        count=len(entries),
        entries=entries,
    )


@app.get("/api/dictionary/search")
async def search_dictionary(q: str):
    """Search dictionary by substring."""
    results = dictionary.search(q)
    return DictionaryListResponse(
        count=len(results),
        entries=results,
    )


# ─── Static files (frontend) ─────────────────────────────────────

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


@app.get("/")
async def serve_index():
    """Serve the main frontend page."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Frontend not yet built. Use /docs for API documentation."}


# Mount static directories
if (FRONTEND_DIR / "css").exists():
    app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
if (FRONTEND_DIR / "js").exists():
    app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")
