# ArSL Transcriber — Master Context File

🚀 **Live Demo:** [https://aslra.onrender.com/](https://aslra.onrender.com/)  
*(Note: The backend is running on a free instance of Render, so it may take up to 50 seconds to wake up on your first request. Please be patient!)*


> **Purpose of this file**: This is the single source of truth for the entire project. Every agent working on this project MUST read this file first. It contains the project goal, architecture, tech stack, phase definitions, phase boundaries, progress tracking, and all decisions made.

---

## 1. Project Overview

**Project Name**: Arabic Sign Language Grammar Discovery & Explainable Transcription Prototype  
**Project Directory**: `C:\Users\rrohi\scratch\arsl-transcriber\`  

### What We Are Building

A research-driven prototype where a user can:
1. Enter an Arabic sentence
2. Get a corresponding Arabic Sign Language (ArSL) gloss sequence
3. See exactly which grammar rules were applied and why
4. See source references for each rule
5. See confidence levels and items requiring expert review

### Core Principles
- **Explainability over accuracy** — every output must trace back to a rule and source
- **Honest uncertainty** — flag what we don't know, never pretend confidence
- **Source-driven** — rules must come from real materials, not invented
- **Traceability** — every rule links to evidence, every evidence links to a source

---

## 2. Tech Stack (FINAL — Approved by User)

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------| 
| **Backend** | FastAPI | 0.116.1 | REST API, rule engine, NLP pipeline |
| **Python** | 3.9+ | 3.9.13 | Runtime |
| **Data Format** | YAML (PyYAML) | 6.0.2 | Rules, sources, dictionary — human-readable, expert-editable |
| **Models** | Pydantic v2 | 2.11.7 | Request/response validation |
| **Server** | Uvicorn | 0.39.0 | ASGI server |
| **Frontend** | HTML + Vanilla CSS + JS | — | No framework, no build step |
| **Frontend Serving** | FastAPI StaticFiles | — | Single `uvicorn` command runs everything |

### Key Dependencies (requirements.txt)
```
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pyyaml>=6.0
pydantic>=2.0
```

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

## 5. Grammar Rules Reference

The transcription engine uses 16 rules across 13 categories. Each rule is backed by cited evidence from our source inventory.

> **Evidence Types:** 🟢 Explicit (directly stated in source) · 🟡 Inferred (pattern observed across examples) · 🔴 Speculative (reasonable guess, no direct evidence)

### R-01 — Topic-Comment Word Order
| | |
|---|---|
| **Category** | Word Order |
| **Confidence** | 🟢 High |
| **Evidence** | 🟢 Explicit |
| **What it does** | ArSL follows a Topic-Comment structure. The subject/topic comes first, then the object/location, then the verb — contrasting Arabic's typical VSO order. |
| **Example** | `ذهب الطالب إلى المدرسة` → `طالب / مدرسة / ذهب` |

---

### R-02 — Time Expression Fronting
| | |
|---|---|
| **Category** | Time |
| **Confidence** | 🟢 High |
| **Evidence** | 🟢 Explicit |
| **What it does** | Time words (yesterday, tomorrow, now, etc.) are moved to the very beginning of the sentence to set the temporal context before anything else. |
| **Example** | `ذهب الطالب إلى المدرسة أمس` → `أمس / طالب / مدرسة / ذهب` |

---

### R-03 — Negation Handling
| | |
|---|---|
| **Category** | Negation |
| **Confidence** | 🟡 Medium |
| **Evidence** | 🟡 Inferred |
| **What it does** | Arabic negation particles (`لم`, `لن`, `لا`, `ما`, `ليس`) are removed and replaced with a single negation sign (`لا`) placed at the end of the clause. A headshake non-manual marker is implied. |
| **Example** | `لم يذهب أحمد إلى المدرسة` → `أحمد / مدرسة / ذهب / لا` |

---

### R-04 — WH-Question Formation
| | |
|---|---|
| **Category** | Question |
| **Confidence** | 🟡 Medium |
| **Evidence** | 🟡 Inferred |
| **What it does** | WH-question words (`أين`, `ماذا`, `من`, `متى`, `كيف`, `لماذا`, `كم`) are moved to the end of the gloss sequence. Accompanied by furrowed eyebrows (non-manual marker). |
| **Example** | `أين تعمل؟` → `عمل / أين` |

---

### R-04b — Yes/No Question Formation
| | |
|---|---|
| **Category** | Question |
| **Confidence** | 🟡 Medium |
| **Evidence** | 🟡 Inferred |
| **What it does** | Yes/No questions keep the same word order as declarative sentences. The particle `هل` is dropped. Meaning is conveyed through non-manual signals (raised eyebrows, forward head tilt). |
| **Example** | `هل أنت طالب؟` → `أنت / طالب [+NMM:سؤال]` |

---

### R-05 — Pronoun Simplification
| | |
|---|---|
| **Category** | Pronoun |
| **Confidence** | 🟡 Medium |
| **Evidence** | 🟡 Inferred |
| **What it does** | Arabic's many pronoun forms (gender, number, case) are simplified to a pointing system — self-point (1st person), forward-point (2nd person), side-point (3rd person). |
| **Example** | `أنا أحب القراءة` → `أنا / قراءة / حب` |

---

### R-06 — Preposition Dropping
| | |
|---|---|
| **Category** | Preposition |
| **Confidence** | 🟢 High |
| **Evidence** | 🟢 Explicit |
| **What it does** | Arabic prepositions (`إلى`, `في`, `من`, `على`, `بـ`, `لـ`, `عن`) are dropped because spatial relationships in ArSL are expressed through sign movement, location, and direction instead. |
| **Example** | `ذهب إلى المدرسة` → `مدرسة / ذهب` |

---

### R-07 — Definite Article (الـ) Dropping
| | |
|---|---|
| **Category** | Article |
| **Confidence** | 🟢 High |
| **Evidence** | 🟢 Explicit |
| **What it does** | The Arabic definite article (`الـ`) is stripped from all words. ArSL does not use articles — definiteness is understood from context. Dictionary entries use the bare/lemma form. |
| **Example** | `المدرسة` → `مدرسة` · `الكتاب` → `كتاب` |

---

### R-08 — Verb Tense Simplification
| | |
|---|---|
| **Category** | Tense |
| **Confidence** | 🟡 Medium |
| **Evidence** | 🟡 Inferred |
| **What it does** | Arabic verb conjugation and tense prefixes (`سـ` for future, `يـ/تـ` for present) are stripped. The verb is signed in its base/root form. Tense is conveyed by a separate time expression already fronted in the sentence. |
| **Example** | `سأشتري` → `مستقبل / شراء` · `ذهبت أمس` → `أمس / ذهب` |

---

### R-09 — Adjective Placement After Noun
| | |
|---|---|
| **Category** | Adjective |
| **Confidence** | 🟡 Medium |
| **Evidence** | 🟡 Inferred |
| **What it does** | Adjectives follow the noun they modify (same as Arabic). Gender/number agreement suffixes are removed — the adjective is signed in its base (masculine singular) form. |
| **Example** | `هذا الكتاب جميل جداً` → `هذا / كتاب / جميل / جداً` |

---

### R-10 — Noun Phrase Simplification
| | |
|---|---|
| **Category** | Noun Phrase |
| **Confidence** | 🔴 Low |
| **Evidence** | 🟡 Inferred |
| **What it does** | Complex noun phrases (demonstratives, possessives, multiple modifiers) are simplified. Order: Demonstrative → Noun → Possessive → Adjective. Articles and case markers are dropped. |
| **Example** | `هذا الكتاب جميل` → `هذا / كتاب / جميل` |

---

### R-11 — Number Before Noun
| | |
|---|---|
| **Category** | Number |
| **Confidence** | 🟡 Medium |
| **Evidence** | 🟡 Inferred |
| **What it does** | Numbers precede the noun they quantify. The noun is always signed in singular form regardless of the number — Arabic's complex number-noun agreement is simplified. |
| **Example** | `ثلاثة كتب` → `ثلاثة / كتاب` · `خمسة طلاب` → `خمسة / طالب` |

---

### R-12 — Non-Manual Markers Annotation
| | |
|---|---|
| **Category** | Non-Manual |
| **Confidence** | 🟢 High |
| **Evidence** | 🟢 Explicit |
| **What it does** | Facial expressions, head movements, and body shifts are essential grammar in ArSL. The engine annotates these with `[+NMM:type]` tags (e.g., `سؤال` for questions, `نفي` for negation). |
| **Example** | `أين تعمل؟` → `عمل / أين [+NMM:سؤال]` |

---

### R-13 — Fingerspelling Fallback
| | |
|---|---|
| **Category** | Fallback |
| **Confidence** | 🟢 High |
| **Evidence** | 🟢 Explicit |
| **What it does** | Words not found in the sign dictionary are fingerspelled using the Arabic manual alphabet. This is standard for proper nouns, technical terms, and new vocabulary. Marked as `fs(word)`. |
| **Example** | `ذهب محمد إلى الجامعة` → `fs(محمد) / جامعة / ذهب` |

---

### R-14 — Conjunction Dropping
| | |
|---|---|
| **Category** | Preposition |
| **Confidence** | 🟡 Medium |
| **Evidence** | 🟡 Inferred |
| **What it does** | Arabic conjunctions (`و`, `ف`, `ثم`, `أو`, `لكن`) are dropped. Sequential actions are shown through temporal sequencing of signs rather than explicit connectors. |
| **Example** | `أكل وشرب` → `أكل / شرب` |

---

### R-15 — Demonstrative Retention
| | |
|---|---|
| **Category** | Noun Phrase |
| **Confidence** | 🟡 Medium |
| **Evidence** | 🟡 Inferred |
| **What it does** | Demonstrative pronouns (`هذا`, `هذه`, `ذلك`, `تلك`) are retained and placed before the noun. Gender/number distinctions are simplified to a near/far distinction only. |
| **Example** | `هذا الكتاب جميل جداً` → `هذا / كتاب / جميل / جداً` |

---

## 6. Phase Definitions & Boundaries

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

## 6. Known Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| CAMeL Tools installation fails on Windows | Backend analyzer degraded | Fallback to regex-based analyzer (documented in Phase 4) |
| Arabic sources are scanned PDFs, not machine-readable | Fewer rules extracted | Note in methodology; use English academic sources as supplement |
| Unified ArSL may have limited documentation | Small rule base | Be transparent about coverage; mark speculative rules |
| Regional ArSL variants conflict with "unified" standard | Confusing rules | Always specify which standard a rule comes from |
| Dictionary too small for real sentences | Many "not found" outputs | Fingerspelling fallback rule; transparent flagging in UI |

---

## 7. How to Run

```bash
# 1. Clone the repository
git clone https://github.com/rrohit1543/Aslra.git
cd Aslra

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# 5. Open in browser
# http://localhost:8000        → Frontend
# http://localhost:8000/docs   → API docs (Swagger UI)
```
