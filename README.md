# ArSL Transcriber — Master Context File

🚀 **Live Demo:** [https://aslra.onrender.com/](https://aslra.onrender.com/)

> **Purpose of this file**: This is the single source of truth for the entire project. Every agent working on this project MUST read this file first. It contains the project goal, architecture, tech stack, phase definitions, phase boundaries, progress tracking, and all decisions made.

---

## 1. Project Overview

**Project Name**: Arabic Sign Language Grammar Discovery & Explainable Transcription Prototype  
**Project Directory**: `C:\Users\rrohi\.gemini\antigravity\scratch\arsl-transcriber\`  
**Status**: 🟡 IN PROGRESS — Phase 0 (Setup)  
**Last Updated**: 2026-06-25T18:35:00+05:30  

### What We Are Building

A research-driven prototype where a user can:
1. Enter an Arabic sentence
2. Get a corresponding Arabic Sign Language (ArSL) gloss sequence
3. See exactly which grammar rules were applied and why
4. See source references for each rule
5. See confidence levels and items requiring expert review

### What We Are NOT Building
- A sign language video generator
- A machine learning model
- A production-ready translator
- A complete Arabic NLP pipeline

### Core Principles
- **Explainability over accuracy** — every output must trace back to a rule and source
- **Honest uncertainty** — flag what we don't know, never pretend confidence
- **Source-driven** — rules must come from real materials, not invented
- **Traceability** — every rule links to evidence, every evidence links to a source

---

## 2. Tech Stack (FINAL — Approved by User)

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Backend** | FastAPI | latest | REST API, rule engine, NLP pipeline |
| **Python** | 3.10+ | — | Runtime |
| **Arabic NLP** | CAMeL Tools | latest | Morphological analysis, tokenization, POS tagging |
| **Data Format** | YAML | — | Rules, sources, dictionary — human-readable, expert-editable |
| **Models** | Pydantic v2 | latest | Request/response validation |
| **Server** | Uvicorn | latest | ASGI server |
| **Frontend** | HTML + Vanilla CSS + JS | — | No framework, no build step |
| **Frontend Serving** | FastAPI StaticFiles | — | Single `uvicorn` command runs everything |

### Key Dependencies (requirements.txt)
```
fastapi
uvicorn[standard]
pyyaml
camel-tools
pydantic>=2.0
```

> **NOTE**: `camel-tools` may require additional setup (Java, model downloads). This is documented in Phase 2.

---

## 3. Directory Structure (FINAL)

```
arsl-transcriber/
│
├── README.md                    # THIS FILE — master context, read first
│
├── backend/
│   ├── main.py                  # FastAPI app entry point, mounts static files, includes routers
│   ├── models.py                # Pydantic models for all request/response schemas
│   ├── tokenizer.py             # Arabic text normalization + tokenization
│   ├── analyzer.py              # Morphological analysis (CAMeL Tools integration)
│   ├── engine.py                # Rule engine — pattern matching + gloss transformation
│   ├── dictionary.py            # Sign dictionary loader + lookup
│   ├── sources.py               # Source registry loader
│   ├── rules_loader.py          # YAML rules loader + validator
│   │
│   └── data/
│       ├── rules.yaml           # Rule base (all grammar rules with evidence)
│       ├── sources.yaml         # Source inventory (all references)
│       └── dictionary.yaml      # Sign dictionary (word → sign entry)
│
├── frontend/
│   ├── index.html               # Main page — RTL layout, input form, output panels
│   ├── css/
│   │   └── styles.css           # Dark mode, RTL-aware, modern design system
│   └── js/
│       └── app.js               # API calls, DOM rendering, output formatting
│
├── docs/
│   ├── source-inventory.md      # Full source inventory with assessments
│   ├── methodology.md           # Answers to all 10 methodology questions
│   ├── limitations.md           # Limitations and risk statement
│   └── test-examples.md         # 5 test examples with full outputs
│
├── requirements.txt             # Python dependencies
└── .gitignore
```

---

## 4. API Design (FINAL)

### Endpoints

| Method | Path | Purpose | Phase |
|--------|------|---------|-------|
| `POST` | `/api/transcribe` | Main endpoint: Arabic sentence → full analysis | Phase 4 |
| `GET` | `/api/rules` | List all rules with evidence and confidence | Phase 4 |
| `GET` | `/api/rules/{rule_id}` | Get single rule detail | Phase 4 |
| `GET` | `/api/sources` | List all sources | Phase 4 |
| `GET` | `/api/dictionary` | Browse/search sign dictionary | Phase 4 |
| `GET` | `/api/health` | Health check | Phase 2 |
| `GET` | `/` | Serve frontend | Phase 5 |

### Core Response Schema (`POST /api/transcribe`)

```json
{
  "input": {
    "original": "ذهب الطالب إلى المدرسة أمس",
    "normalized": "ذهب الطالب الى المدرسه امس"
  },
  "tokenization": [
    {
      "token": "ذهب",
      "pos": "VERB",
      "lemma": "ذهب",
      "features": {"tense": "past"},
      "has_article": false,
      "prefix": null,
      "suffix": null
    }
  ],
  "applied_rules": [
    {
      "rule_id": "R-01",
      "rule_name": "Time expression fronting",
      "description": "Moved أمس to the front of the gloss sequence",
      "evidence_type": "explicit",
      "confidence": "medium",
      "sources": [
        {"source_id": "S-01", "title": "...", "page": "..."}
      ]
    }
  ],
  "gloss_sequence": [
    {
      "gloss": "أمس",
      "original_word": "أمس",
      "in_dictionary": true,
      "dictionary_note": "Standard UASL sign"
    }
  ],
  "gloss_string": "أمس / طالب / مدرسة / ذهب",
  "confidence": {
    "level": "medium",
    "explanation": "Time fronting is well-attested; preposition dropping has medium evidence"
  },
  "expert_review_items": [
    "Whether مدرسة has a standard sign in the selected dictionary",
    "Whether ذهب requires an explicit past-tense marker"
  ]
}
```

---

## 5. Phase Definitions & Boundaries

### PHASE 0: Project Setup ✅ → 🟡
**Owner**: Any agent  
**Start condition**: Project directory created  
**End condition**: All files/folders exist (empty stubs OK), requirements.txt written, README complete  
**Deliverables**:
- [x] README.md (this file)
- [ ] Directory structure created (all folders)
- [ ] requirements.txt
- [ ] Empty stub files for all Python modules
- [ ] Empty stub files for frontend
- [ ] .gitignore

**Boundary rule**: Phase 0 agent must NOT write any logic. Only create structure and stubs.

---

### PHASE 1: Source Discovery 🔴 NOT STARTED
**Owner**: Research agent  
**Start condition**: Phase 0 complete  
**End condition**: `docs/source-inventory.md` is complete with ≥8 sources, `backend/data/sources.yaml` has structured entries  
**Deliverables**:
- [ ] `docs/source-inventory.md` — full source inventory table
- [ ] `backend/data/sources.yaml` — machine-readable source registry
- [ ] At least 8 sources found (mix of Arabic + English)
- [ ] At least 3 Arabic-language sources
- [ ] Each source classified by type (dictionary/grammar/teaching/academic/institutional/community)
- [ ] Each source assessed for credibility
- [ ] Each source mapped to which rules it supports

**Search queries to execute** (minimum):

English:
1. `"Unified Arabic Sign Language" grammar rules`
2. `"Arabic Sign Language" sentence structure gloss`
3. `ArSL word order syntax morphology`
4. `"Arabic Sign Language" dictionary PDF`
5. `"Arabic Sign Language" linguistic analysis`

Arabic:
6. `قواعد لغة الإشارة العربية الموحدة`
7. `ترتيب الجملة في لغة الإشارة العربية`
8. `معجم لغة الإشارة العربية الموحدة`
9. `تعليم لغة الإشارة للصم العرب`
10. `نحو لغة الإشارة العربية بنية الجملة`

Institutional sites to check:
11. Arab League / ALECSO sign language initiatives
12. Saudi/Egyptian/Jordanian deaf associations
13. King Saud University, Cairo University repositories
14. World Federation of the Deaf — Arab region

**Source YAML schema**:
```yaml
- id: S-XX
  title: Source title
  language: ar | en | both
  url: URL or "offline"
  acquisition_method: web | pdf_download | book | app
  type: dictionary | grammar | teaching | academic | institutional | community
  credibility: high | medium | low
  credibility_reason: Why we trust/distrust it
  rules_supported: [R-01, R-03, ...]
  limitations: Known gaps or biases
  year: Publication year if known
  author: Author/organization
```

**Boundary rule**: Phase 1 agent must NOT write any Python code or frontend code. Only research and write documentation/data files.

---

### PHASE 2: Rule Extraction 🔴 NOT STARTED
**Owner**: Research agent (can be same as Phase 1)  
**Start condition**: Phase 1 complete (source inventory exists with ≥8 sources)  
**End condition**: `backend/data/rules.yaml` has ≥12 rules covering ≥8 categories, each with evidence  
**Deliverables**:
- [ ] `backend/data/rules.yaml` — full rule base
- [ ] ≥12 rules extracted
- [ ] Rules cover ≥8 of the 13 categories listed below
- [ ] Each rule has evidence_type: explicit | inferred | speculative
- [ ] Each rule links to ≥1 source from sources.yaml
- [ ] Each rule has ≥1 example (input → output)

**Rule categories** (target ≥8 of these 13):
1. Word order (Topic-Comment / SOV)
2. Time expression fronting
3. Negation
4. Questions (WH and yes/no)
5. Pronouns
6. Preposition handling
7. Definite article (الـ) dropping
8. Verb tense / aspect
9. Adjective placement
10. Noun phrase structure
11. Numerical expressions
12. Non-manual markers (facial expressions)
13. Fallback for unknown words

**Rule YAML schema**:
```yaml
- id: R-XX
  name: Human-readable name
  category: word_order | time | negation | question | pronoun | preposition | article | tense | adjective | noun_phrase | number | non_manual | fallback
  description: What the rule does
  trigger: Condition that activates the rule (natural language + keywords)
  action: Transformation applied (natural language description)
  evidence_type: explicit | inferred | speculative
  evidence:
    - source_id: S-XX
      page_or_section: Page or section reference
      quote_or_summary: What the source says (Arabic or English)
  confidence: high | medium | low
  priority: integer (lower = applied first)
  examples:
    - input: "Arabic sentence"
      output: "gloss / sequence"
      explanation: "Step-by-step"
  notes: Caveats and uncertainties
  requires_expert_review: true | false
  review_questions:
    - Specific question for domain experts
```

**Boundary rule**: Phase 2 agent must NOT write Python logic or frontend code. Only produce `rules.yaml` and update `sources.yaml` if new sources were found during rule extraction.

---

### PHASE 3: Dictionary Construction 🔴 NOT STARTED
**Owner**: Research agent or build agent  
**Start condition**: Phase 2 complete (rules.yaml exists)  
**End condition**: `backend/data/dictionary.yaml` has ≥150 entries covering all words used in test examples  
**Deliverables**:
- [ ] `backend/data/dictionary.yaml` — sign dictionary
- [ ] ≥150 entries
- [ ] All words in the 5 test examples are covered
- [ ] Each entry has source attribution
- [ ] Unknown words flagged with `verified: false`

**Dictionary YAML schema**:
```yaml
- word: Arabic word (lemma form)
  sign_gloss: Sign title/gloss (Arabic)
  category: noun | verb | adjective | adverb | pronoun | number | time | question_word | negation | preposition | connector | other
  verified: true | false
  source_id: S-XX
  notes: Any special notes about this sign
  regional_variants: Optional list of regional differences
```

**Boundary rule**: Phase 3 agent must NOT write Python logic or frontend code. Only produce dictionary.yaml.

---

### PHASE 4: Backend Implementation 🔴 NOT STARTED
**Owner**: Build agent  
**Start condition**: Phases 1-3 complete (sources.yaml, rules.yaml, dictionary.yaml all exist and populated)  
**End condition**: All API endpoints work, `uvicorn backend.main:app` starts without errors, POST /api/transcribe returns correct structured response for all 5 test examples  
**Deliverables**:
- [ ] `backend/main.py` — FastAPI app with all routes
- [ ] `backend/models.py` — Pydantic models
- [ ] `backend/tokenizer.py` — Arabic tokenization
- [ ] `backend/analyzer.py` — Morphological analysis
- [ ] `backend/engine.py` — Rule engine
- [ ] `backend/dictionary.py` — Dictionary loader + lookup
- [ ] `backend/sources.py` — Sources loader
- [ ] `backend/rules_loader.py` — Rules loader + validator
- [ ] All 5 test examples produce correct output via API
- [ ] `/api/health` returns 200

**Implementation order within Phase 4**:
1. `models.py` — define all Pydantic schemas first
2. `rules_loader.py` + `sources.py` + `dictionary.py` — data loaders
3. `tokenizer.py` — text normalization + splitting
4. `analyzer.py` — morphological analysis (CAMeL Tools or fallback)
5. `engine.py` — rule matching + transformation
6. `main.py` — wire everything together, define routes

**CAMeL Tools fallback plan**: If CAMeL Tools installation fails or is too complex, implement a simplified Python-based analyzer that handles:
- Definite article (الـ) stripping
- Common prefix detection (سـ, وـ, بـ, فـ, لـ, كـ)
- Common suffix detection (ة, ات, ين, ون)
- Basic POS guessing from word patterns
- This is acceptable for a prototype — document the limitation

**Boundary rule**: Phase 4 agent must NOT modify any YAML data files. If data issues are found, document them and report back — do not fix data files directly.

---

### PHASE 5: Frontend Implementation 🔴 NOT STARTED
**Owner**: Build agent  
**Start condition**: Phase 4 complete (API works for all test examples)  
**End condition**: Frontend loads at `/`, user can type Arabic, submit, and see full structured output  
**Deliverables**:
- [ ] `frontend/index.html` — main page
- [ ] `frontend/css/styles.css` — styling
- [ ] `frontend/js/app.js` — API integration + rendering
- [ ] RTL text direction works
- [ ] All 7 output sections render (input echo, tokenization, rules, gloss, dictionary status, evidence, expert review)
- [ ] Works in Chrome and Firefox

**UI sections** (all required):
1. **Header** — project title + description
2. **Input** — RTL textarea + submit button
3. **Original Input** — echo of what was typed
4. **Tokenization Table** — word | POS | lemma | features
5. **Applied Rules** — rule ID, name, description, evidence badge (🟢🟡🔴)
6. **Gloss Sequence** — large, prominent, RTL, with `/` separators
7. **Dictionary Status** — per-word: ✅ in dictionary | ⚠️ inferred | ❌ not found
8. **Evidence & Sources** — collapsible, per-rule source citations
9. **Confidence Level** — overall assessment with explanation
10. **Expert Review Items** — flagged questions for human experts

**Boundary rule**: Phase 5 agent must NOT modify backend Python files or YAML data files. Frontend only.

---

### PHASE 6: Documentation & Verification 🔴 NOT STARTED
**Owner**: Any agent  
**Start condition**: Phases 4 and 5 complete  
**End condition**: All 4 docs complete, all 5 test examples verified  
**Deliverables**:
- [ ] `docs/methodology.md` — answers all 10 methodology questions
- [ ] `docs/source-inventory.md` — formatted version of sources.yaml
- [ ] `docs/limitations.md` — limitations and risk statement
- [ ] `docs/test-examples.md` — 5 test examples with full captured output
- [ ] All 5 test examples run successfully end-to-end

**Methodology questions to answer** (section 3.4 of the assignment):
1. How did you discover the source materials?
2. What search queries did you use? (list Arabic + English queries)
3. How did you evaluate source credibility?
4. How did you handle scanned PDFs / OCR?
5. How did you extract rules from sources?
6. Which rules are explicit vs. inferred?
7. Did you use RAG? If so, how?
8. How did you prevent hallucinated grammar rules?
9. How did you handle missing dictionary words?
10. How would expert review update the rule base?

**5 test examples** (FINAL — all agents must use these):

| # | Arabic Input | Expected Patterns |
|---|-------------|-------------------|
| 1 | `ذهب الطالب إلى المدرسة أمس` | Time fronting, preposition drop, article strip |
| 2 | `لم يذهب أحمد إلى المدرسة` | Negation, preposition drop |
| 3 | `أين تعمل؟` | WH-question handling |
| 4 | `سأشتري ثلاثة كتب غداً` | Future tense, number, time fronting |
| 5 | `هذا الكتاب جميل جداً` | Demonstrative, adjective, intensifier |

**Boundary rule**: Phase 6 agent must NOT modify any code or data files. Documentation and verification only. If bugs are found, report them — do not fix.

---

## 6. Progress Tracker

| Phase | Status | Started | Completed | Agent/Notes |
|-------|--------|---------|-----------|-------------|
| Phase 0: Setup | 🟡 In Progress | 2026-06-25 | — | Creating structure |
| Phase 1: Source Discovery | 🔴 Not Started | — | — | — |
| Phase 2: Rule Extraction | 🔴 Not Started | — | — | — |
| Phase 3: Dictionary | 🔴 Not Started | — | — | — |
| Phase 4: Backend | 🔴 Not Started | — | — | — |
| Phase 5: Frontend | 🔴 Not Started | — | — | — |
| Phase 6: Documentation | 🔴 Not Started | — | — | — |

---

## 7. Decisions Log

All significant decisions made during the project:

| # | Date | Decision | Rationale | Decided By |
|---|------|----------|-----------|------------|
| D-01 | 2026-06-25 | Use FastAPI backend | User preference + enables CAMeL Tools for Arabic NLP | User |
| D-02 | 2026-06-25 | Vanilla HTML/CSS/JS frontend | No build step, fast iteration, assignment doesn't require framework | Agent + User |
| D-03 | 2026-06-25 | Serve frontend via FastAPI StaticFiles | Single `uvicorn` command to run everything | Agent |
| D-04 | 2026-06-25 | Rule engine (not LLM) for runtime transcription | Explainability requirement — every output must trace to a rule | Agent |
| D-05 | 2026-06-25 | YAML for all data files | Human-readable, expert-editable, easy to review | Agent |
| D-06 | 2026-06-25 | CAMeL Tools with fallback to simple analyzer | Best available Arabic NLP, but may have install issues | Agent |

---

## 8. Known Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| CAMeL Tools installation fails on Windows | Backend analyzer degraded | Fallback to regex-based analyzer (documented in Phase 4) |
| Arabic sources are scanned PDFs, not machine-readable | Fewer rules extracted | Note in methodology; use English academic sources as supplement |
| Unified ArSL may have limited documentation | Small rule base | Be transparent about coverage; mark speculative rules |
| Regional ArSL variants conflict with "unified" standard | Confusing rules | Always specify which standard a rule comes from |
| Dictionary too small for real sentences | Many "not found" outputs | Fingerspelling fallback rule; transparent flagging in UI |

---

## 9. Agent Instructions

### Before starting any phase:
1. Read this entire README.md
2. Check the Progress Tracker (section 6) — only start a phase if its prerequisite is ✅
3. Respect your phase boundary — do NOT modify files outside your phase scope
4. Update the Progress Tracker when you start and finish

### When finishing a phase:
1. Update the Progress Tracker in this README
2. List what you completed and what (if anything) is incomplete
3. Note any issues or blockers for the next phase

### If you find a problem in a previous phase's output:
1. Do NOT fix it yourself (unless it's a trivial typo)
2. Document the problem clearly
3. Report it so the appropriate phase agent can fix it

### File ownership by phase:

| File(s) | Owner Phase | Other Phases May Read | Other Phases May Write |
|---------|-------------|----------------------|----------------------|
| README.md | Phase 0 | All | Phase 6 (progress updates only) |
| backend/data/*.yaml | Phases 1-3 | Phases 4-6 | ❌ No |
| backend/*.py | Phase 4 | Phases 5-6 | ❌ No |
| frontend/* | Phase 5 | Phase 6 | ❌ No |
| docs/* | Phases 1-2, 6 | All | ❌ No |
| requirements.txt | Phase 0, 4 | All | ❌ No |

---

## 10. How to Run (for verification agents)

```bash
# 1. Navigate to project root
cd C:\Users\rrohi\.gemini\antigravity\scratch\arsl-transcriber

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 5. Open in browser
# http://localhost:8000        → Frontend
# http://localhost:8000/docs   → API docs (Swagger UI)
```

---

*End of context file. All agents must read this before beginning work.*
