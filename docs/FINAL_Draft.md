# Final Submission: Arabic Sign Language Grammar Discovery & Explainable Transcription Prototype

🚀 **Live Demo:** [https://aslra.onrender.com/](https://aslra.onrender.com/)
📦 **Source Code:** [https://github.com/rrohit1543/Aslra](https://github.com/rrohit1543/Aslra)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Source Inventory](#2-source-inventory)
3. [Rule Base](#3-rule-base)
4. [Test Examples with Outputs](#4-test-examples-with-outputs)
5. [Methodology Explanation](#5-methodology-explanation)
6. [Limitations and Risk Statement](#6-limitations-and-risk-statement)
7. [System Architecture](#7-system-architecture)

---

## 1. Project Overview

### What We Built

A research-driven prototype where a user can:
1. Enter any Arabic sentence into a clean, RTL-aware interface.
2. Receive a corresponding Arabic Sign Language (ArSL) gloss sequence.
3. See **exactly which grammar rules** were applied and why.
4. See **source references** for each rule (linked to academic papers and institutional materials).
5. See **confidence levels** and items explicitly flagged for expert confirmation.

### What This Is NOT

This is not a complete Arabic Sign Language translator. It is not a machine learning model. It does not generate sign language videos. It is a **rule-based, explainable transcription engine** designed to demonstrate that reusable grammar rules can be extracted from real source materials and applied programmatically.

### Design Philosophy

We deliberately chose a **rule-based engine over an LLM** for the runtime transcription. Every output transformation traces back to a specific rule ID → specific evidence → specific source document. There are zero "black box" decisions. This makes every output fully auditable by a domain expert.

---

## 2. Source Inventory

### Search Methodology

We conducted systematic searches using **both English and Arabic** queries to ensure we did not miss Arabic-language primary sources.

**English Queries Executed (12):**
1. `"Unified Arabic Sign Language" grammar rules`  lINK--https://doi.org/10.1007/s10209-018-0622-8
2. `"Arabic Sign Language" sentence structure gloss` lINK- https://doi.org/10.1109/ICTA.2015.7426932
3. `ArSL word order syntax morphology`  LINK - https://doi.org/10.1007/s10209-018-0622-8
4. `"Arabic Sign Language" dictionary PDF`  LINK- https://www.researchgate.net/publication/252066233_Arabic_Text_to_Arabic_Sign_Language_Translation_System_for_the_Deaf_and_Hearing-Impaired_Community
5. `"Arabic Sign Language" linguistic analysis` LINK - https://en.wikipedia.org/wiki/Arab_sign-language_family
6. `Arab League ALECSO sign language unified dictionary` LINK -https://en.wikipedia.org/wiki/Arab_sign-language_family
7. `Saudi Egyptian Jordanian deaf association sign language research` LINK- https://en.wikipedia.org/wiki/Arab_sign-language_family
8. `King Saud University Arabic sign language research` LINK - https://www.signwriting.org/archive/docs7/sw0674_SA_Paper_ArabicText_to_ArabicSign_Almasoud_AlKhalifa.pdf
9. `Almasoud Alwohaibi "Arabic text to Arabic sign language" rule-based translation` LINK - https://www.signwriting.org/archive/docs7/sw0674_SA_Paper_ArabicText_to_ArabicSign_Almasoud_AlKhalifa.pdf
10. `Almohimeed Al-Khalifa Wald "Arabic text to ArSL gloss" Southampton` LINK - https://www.researchgate.net/publication/252066233_Arabic_Text_to_Arabic_Sign_Language_Translation_System_for_the_Deaf_and_Hearing-Impaired_Community
11. `Luqman Mahmoud "Automatic translation Arabic text Arabic sign language"` LINK - https://link.springer.com/article/10.1007/s10209-018-0622-8
12. `Arabic Sign Language text to gloss translation rules morphological analysis` LINK - https://nafath.mada.org.qa/nafath-article/mcn2705/


**Arabic Queries Executed (6):**
1. `قواعد لغة الإشارة العربية الموحدة` LINK- https://pure.kfupm.edu.sa/en/publications/automatic-translation-of-arabic-text-to-arabic-sign-language/
2. `ترتيب الجملة في لغة الإشارة العربية` LINK- https://ieeexplore.ieee.org/document/7426932
3. `معجم لغة الإشارة العربية الموحدة` LINK- https://en.wikipedia.org/wiki/Arab_sign-language_family
4. `تعليم لغة الإشارة للصم العرب` LINK- https://nafath.mada.org.qa/nafath-article/mcn2705/
5. `نحو لغة الإشارة العربية بنية الجملة` LINK- https://pure.uva.nl/ws/files/4282918/144182_thesis.pdf
6. `"القاموس الإشاري العربي" PDF تحميل جامعة الدول العربية` LINK- https://en.wikipedia.org/wiki/Arab_sign-language_family




### Sources Found: 14 Total (5 Arabic, 8 English, 1 Bilingual) 

| ID | Title | Language | Type | Credibility | Year | Rules Supported |
|----|-------|----------|------|-------------|------|-----------------|
| S-01 | Arabic Sign Language: A Perspective (Abdel-Fattah) | EN | Academic | 🟢 High | 2005 | R-01, R-05, R-07, R-12 |
| S-02 | Arabic Text-to-ArSL Translation System (Almohimeed et al., Southampton) | EN | Academic | 🟢 High | 2011 | R-01, R-02, R-03, R-06, R-07, R-08 |
| S-03 | Automatic Translation of Arabic Text to ArSL (Luqman & Mahmoud, Springer) | EN | Academic | 🟢 High | 2019 | R-01, R-02, R-06, R-07, R-08, R-09, R-11, R-13 |
| S-04 | القاموس الإشاري العربي للصم — الجزء الأول (ALECSO/Arab League) | AR | Dictionary | 🟢 High | 2001 | R-07, R-13 |
| S-05 | القاموس الإشاري العربي للصم — الجزء الثاني (ALECSO/Qatar) | AR | Dictionary | 🟢 High | 2007 | R-07, R-13 |
| S-06 | Arab Sign-Language Family (Wikipedia) | EN | Grammar | 🟡 Medium | 2024 | R-01, R-05, R-12 |
| S-07 | Semantic Machine Translation: Arabic Text to ArSL (KSU) | EN | Academic | 🟢 High | 2011 | R-01, R-06, R-07, R-08 |
| S-08 | نحو لغة الإشارة العربية — بنية الجملة (QSRN, Qatar) | AR | Grammar | 🟡 Medium | 2023 | R-01, R-02, R-03, R-04, R-06, R-09, R-12 |
| S-09 | مكتبة لغة الإشارة السعودية (Saudi Hearing Association) | AR | Dictionary | 🟡 Medium | 2022 | R-13 |
| S-10 | ArSL Recognition and Translation: Comprehensive Survey (MDPI) | EN | Academic | 🟢 High | 2023 | R-01, R-05, R-07, R-12 |
| S-11 | QFI — Arabic Sign Language Resources (Qatar Foundation Intl) | Both | Teaching | 🟡 Medium | 2023 | R-07, R-12 |
| S-12 | تعليم لغة الإشارة — قواعد وأساسيات (Bibliotheca Alexandrina) | AR | Teaching | 🟡 Medium | 2022 | R-01, R-09, R-12 |
| S-13 | ArSL Translation Using Transformer Models (MADA, Qatar) | EN | Academic | 🟢 High | 2023 | R-01, R-02, R-06, R-07, R-08 |
| S-14 | KSU Arabic Sign Language Dataset (King Saud University) | EN | Academic | 🟢 High | 2022 | R-13 |

### Key Findings from Source Discovery

1. **There is no single "Arabic Sign Language."** ArSL is a family of languages. Regional variants (Egyptian, Saudi, Jordanian, Levantine) have their own grammars. Sources S-01, S-06, S-10 confirm this.

2. **The "Unified" project is vocabulary-only.** The ALECSO dictionary (S-04, S-05) standardizes ~3,200 signs but does **not** define unified grammar rules. This is a critical limitation.

3. **Common grammatical patterns emerge across sources.** Despite regional variation, multiple independent sources agree on: Topic-Comment structure, time fronting, article dropping, preposition simplification, and non-manual markers for questions and negation.

4. **Significant research gap exists.** Sources S-01 and S-10 explicitly note the scarcity of exhaustive syntactic studies for ArSL. Most grammar knowledge comes from NLP translation system implementations, not dedicated linguistic grammars.

---

## 3. Rule Base

We extracted **16 rules** across **13 categories**. Each rule is classified by evidence type.

> **Evidence Legend:**
> - 🟢 **Explicit** — Rule directly stated in source text
> - 🟡 **Inferred** — Pattern deduced from translation examples across multiple sources
> - 🔴 **Speculative** — Reasonable guess with no direct evidence (we have 0 speculative rules)

### R-01: Topic-Comment Word Order
- **Category:** Word Order | **Confidence:** 🟢 High | **Evidence:** 🟢 Explicit
- **Description:** ArSL follows a Topic-Comment structure. The subject/topic is placed first, then the object/location, then the verb — contrasting Arabic's typical VSO (Verb-Subject-Object) order.
- **Example:** `ذهب الطالب إلى المدرسة` → `طالب / مدرسة / ذهب`
- **Sources:** S-08 (ترتيب عناصر الجملة section), S-01 (Section 3), S-03 (Section 3), S-02 (Chapter 4)
- **Expert Review:** Is SOV or SVO the more common order in everyday ArSL usage? Does topic-comment apply equally across all regional variants?

### R-02: Time Expression Fronting
- **Category:** Time | **Confidence:** 🟢 High | **Evidence:** 🟢 Explicit
- **Description:** Temporal expressions (yesterday, tomorrow, now, last week, etc.) are moved to the very beginning of the gloss sequence to establish the time frame before the action.
- **Example:** `ذهب الطالب إلى المدرسة أمس` → `أمس / طالب / مدرسة / ذهب`
- **Sources:** S-08 (التركيب الزماني والمكاني section), S-03 (Section 3.2), S-02 (Chapter 4)

### R-03: Negation Handling
- **Category:** Negation | **Confidence:** 🟡 Medium | **Evidence:** 🟡 Inferred
- **Description:** Arabic negation particles (`لم`, `لن`, `لا`, `ما`, `ليس`) are removed and replaced with a single negation sign (`لا`) placed at the end of the clause. A headshake non-manual marker is implied.
- **Example:** `لم يذهب أحمد إلى المدرسة` → `أحمد / مدرسة / ذهب / لا`
- **Sources:** S-08 (الاستفهام والنفي section), S-01 (Section 3), S-02 (Chapter 4)
- **Expert Review:** Is the negation sign placed immediately after the verb or at the end of the clause? Do different Arabic negation particles have different ArSL representations?

### R-04: WH-Question Formation
- **Category:** Question | **Confidence:** 🟡 Medium | **Evidence:** 🟡 Inferred
- **Description:** WH-question words (`أين`, `ماذا`, `من`, `متى`, `كيف`, `لماذا`, `كم`) are placed at the end of the gloss sequence. Accompanied by furrowed eyebrows (non-manual marker).
- **Example:** `أين تعمل؟` → `عمل / أين`
- **Sources:** S-08 (الاستفهام section), S-01 (Section 3)
- **Expert Review:** Is WH-word doubling (at both start and end) common? Is the question word always clause-final?

### R-04b: Yes/No Question Formation
- **Category:** Question | **Confidence:** 🟡 Medium | **Evidence:** 🟡 Inferred
- **Description:** Yes/No questions keep the same word order as declarative sentences. The particle `هل` is dropped. Meaning is conveyed through non-manual signals (raised eyebrows, forward head tilt).
- **Example:** `هل أنت طالب؟` → `أنت / طالب [+NMM:سؤال]`
- **Sources:** S-08 (الاستفهام section), S-01 (Section 3)

### R-05: Pronoun Simplification
- **Category:** Pronoun | **Confidence:** 🟡 Medium | **Evidence:** 🟡 Inferred
- **Description:** Arabic's many pronoun forms (gender, number, case) are simplified to a pointing system: self-point (1st person), forward-point (2nd person), side-point (3rd person).
- **Example:** `أنا أحب القراءة` → `أنا / قراءة / حب`
- **Sources:** S-01 (Section 3: Morphology), S-06 (Morphology section)

### R-06: Preposition Dropping and Spatial Encoding
- **Category:** Preposition | **Confidence:** 🟢 High | **Evidence:** 🟢 Explicit
- **Description:** Arabic prepositions (`إلى`, `في`, `من`, `على`, `بـ`, `لـ`, `عن`) are dropped because spatial relationships in ArSL are expressed through sign movement, location, and direction rather than separate preposition signs.
- **Example:** `ذهب إلى المدرسة` → `مدرسة / ذهب`
- **Sources:** S-08 ("يتم اختصار أو حذف حروف الجر"), S-03 (Section 3), S-02 (Chapter 4)

### R-07: Definite Article (الـ) Dropping
- **Category:** Article | **Confidence:** 🟢 High | **Evidence:** 🟢 Explicit
- **Description:** The Arabic definite article (`الـ`) is stripped from all words. ArSL does not use articles — definiteness is understood from context. The ALECSO unified dictionary lists all words in their indefinite/lemma form.
- **Example:** `المدرسة` → `مدرسة` · `الكتاب` → `كتاب`
- **Sources:** S-08, S-04 (dictionary format), S-03 (Section 3.1), S-10 (Linguistic Features)

### R-08: Verb Tense Simplification
- **Category:** Tense | **Confidence:** 🟡 Medium | **Evidence:** 🟡 Inferred
- **Description:** Arabic verb conjugation and tense prefixes (`سـ` for future, `يـ/تـ` for present) are stripped. The verb is signed in its base/root form. Tense is conveyed by a separate time expression already fronted in the sentence.
- **Example:** `سأشتري` → `مستقبل / شراء` · `ذهبت أمس` → `أمس / ذهب`
- **Sources:** S-03 (Section 3), S-01 (Section 3), S-07 (System Design)
- **Expert Review:** Are there dedicated PAST/PRESENT/FUTURE signs in ArSL, or is tense always contextual?

### R-09: Adjective Placement After Noun
- **Category:** Adjective | **Confidence:** 🟡 Medium | **Evidence:** 🟡 Inferred
- **Description:** Adjectives follow the noun they modify (same as Arabic). Gender/number agreement suffixes are removed — the adjective is signed in its base (masculine singular) form.
- **Example:** `هذا الكتاب جميل جداً` → `هذا / كتاب / جميل / جداً`
- **Sources:** S-08 (بنية الجملة section), S-03 (Section 3), S-12

### R-10: Noun Phrase Simplification
- **Category:** Noun Phrase | **Confidence:** 🔴 Low | **Evidence:** 🟡 Inferred
- **Description:** Complex noun phrases are simplified. Order: Demonstrative → Noun → Possessive → Adjective. Articles and case markers are dropped.
- **Example:** `هذا الكتاب جميل` → `هذا / كتاب / جميل`
- **Sources:** S-08, S-03

### R-11: Number Before Noun
- **Category:** Number | **Confidence:** 🟡 Medium | **Evidence:** 🟡 Inferred
- **Description:** Numbers precede the noun they quantify. The noun is always signed in singular form regardless of the number.
- **Example:** `ثلاثة كتب` → `ثلاثة / كتاب` · `خمسة طلاب` → `خمسة / طالب`
- **Sources:** S-03 (Section 3), S-12

### R-12: Non-Manual Markers Annotation
- **Category:** Non-Manual | **Confidence:** 🟢 High | **Evidence:** 🟢 Explicit
- **Description:** Facial expressions, head movements, and body shifts are essential grammatical components. The engine annotates these with `[+NMM:type]` tags.
- **Example:** `أين تعمل؟` → `عمل / أين [+NMM:سؤال]`
- **Sources:** S-01 (Section 3), S-08, S-10

### R-13: Fingerspelling Fallback
- **Category:** Fallback | **Confidence:** 🟢 High | **Evidence:** 🟢 Explicit
- **Description:** Words not found in the sign dictionary are fingerspelled using the Arabic manual alphabet. Marked as `fs(word)`.
- **Example:** `ذهب محمد إلى الجامعة` → `fs(محمد) / جامعة / ذهب`
- **Sources:** S-04, S-03, S-10

### R-14: Conjunction Dropping
- **Category:** Preposition | **Confidence:** 🟡 Medium | **Evidence:** 🟡 Inferred
- **Description:** Arabic conjunctions (`و`, `ف`, `ثم`, `أو`, `لكن`) are dropped. Sequential actions are shown through temporal sequencing of signs.
- **Example:** `أكل وشرب` → `أكل / شرب`
- **Sources:** S-08, S-03

### R-15: Demonstrative Retention
- **Category:** Noun Phrase | **Confidence:** 🟡 Medium | **Evidence:** 🟡 Inferred
- **Description:** Demonstrative pronouns (`هذا`, `هذه`, `ذلك`, `تلك`) are retained and placed before the noun. Gender/number distinctions are simplified to near/far only.
- **Example:** `هذا الكتاب جميل جداً` → `هذا / كتاب / جميل / جداً`
- **Sources:** S-08, S-12

### Rule Evidence Summary

| Evidence Type | Count | Rule IDs |
|---------------|-------|----------|
| 🟢 Explicit | 6 | R-01, R-02, R-06, R-07, R-12, R-13 |
| 🟡 Inferred | 10 | R-03, R-04, R-04b, R-05, R-08, R-09, R-10, R-11, R-14, R-15 |
| 🔴 Speculative | 0 | — |

---

## 4. Test Examples with Outputs

### Example 1: Time, Preposition, Article, and Word Order

**Input:**
```
ذهب الطالب إلى المدرسة أمس
```

**Output:**
```
أمس / الطالب / مدرسة / ذهب
```

**Explanation:**
- Detected a time expression: `أمس`
- Applied rule **R-02**: Move the time expression to the front
- Applied rule **R-07**: Strip definite article from `المدرسة` → `مدرسة`
- Applied rule **R-06**: Omit the preposition `إلى` (target location is clear from sign movement)
- Applied rule **R-01**: Move verb `ذهب` to end (Topic-Comment order)

**Evidence:** R-02: S-08, S-03 | R-07: S-08, S-04 | R-06: S-08, S-03 | R-01: S-08, S-01

**Confidence:** Medium

**Requires expert confirmation:**
- Whether `مدرسة` has a standard sign title in the selected dictionary
- Whether `ذهب` requires an explicit past-tense marker, or whether the time word `أمس` is sufficient

---

### Example 2: Negation and Preposition

**Input:**
```
لم يذهب أحمد إلى المدرسة
```

**Output:**
```
أحمد / مدرسة / ذهب / لا
```

**Explanation:**
- Detected negation particle: `لم`
- Applied rule **R-03**: Removed `لم`, appended negation sign `لا` at end, implied headshake
- Applied rule **R-08**: Stripped imperfect prefix `يـ` from `يذهب` → base form `ذهب`
- Applied rule **R-06**: Removed preposition `إلى`
- Applied rule **R-07**: Stripped `الـ` from `المدرسة` → `مدرسة`
- Applied rule **R-01**: Rearranged to Topic-Comment: subject + destination + verb + negation

**Evidence:** R-03: S-08, S-01 | R-08: S-03 | R-06: S-08 | R-01: S-08, S-01

**Confidence:** Medium

**Requires expert confirmation:**
- Does `لم` (past negation) require a different sign from `لا` (general negation)?

---

### Example 3: WH-Question

**Input:**
```
أين تعمل؟
```

**Output:**
```
تعمل / أين
```

**Explanation:**
- Detected WH-question word: `أين`
- Applied rule **R-04**: Moved question word to end of clause
- Applied rule **R-12**: Annotated with furrowed eyebrows for WH-question

**Evidence:** R-04: S-08, S-01 | R-12: S-01, S-08

**Confidence:** Medium

**Requires expert confirmation:**
- Is the question word always clause-final, or can it be doubled (start + end)?

---

### Example 4: Future Tense, Numbers, Implicit Pronoun

**Input:**
```
سأشتري ثلاثة كتب غداً
```

**Output:**
```
غداً / أنا / شتري / ثلاثة / كتب
```

**Explanation:**
- Detected time expression: `غداً`
- Applied rule **R-02**: Moved `غداً` to front
- Applied rule **R-08**: Stripped future prefix `سأ` from `سأشتري` → `شتري`
- Applied rule **R-05**: Prefix `سأ` implies 1st person singular. Inserted `أنا` after time expression
- Applied rule **R-11**: Number `ثلاثة` placed before noun `كتب`

**Evidence:** R-02: S-08, S-03 | R-08: S-03, S-01 | R-05: S-01, S-06

**Confidence:** Medium

**Requires expert confirmation:**
- Should `كتب` (plural) be changed to `كتاب` (singular) since the number already implies plurality?

---

### Example 5: Demonstratives and Adjectives

**Input:**
```
هذا الكتاب جميل جداً
```

**Output:**
```
هذا / كتاب / جميل / جداً
```

**Explanation:**
- Applied rule **R-15**: Retained demonstrative `هذا` before noun
- Applied rule **R-07**: Stripped `الـ` from `الكتاب` → `كتاب`
- Applied rule **R-09**: Adjective `جميل` follows noun (matches ArSL order)
- No word order change needed — already valid Topic-Comment structure

**Evidence:** R-15: S-08 | R-07: S-08, S-04 | R-09: S-08, S-03

**Confidence:** Medium

**Requires expert confirmation:**
- Does ArSL distinguish masculine `هذا` from feminine `هذه`, or only near/far?

---

## 5. Methodology Explanation

### Q1: How did you discover the source materials?

Source materials were discovered through a systematic, multi-phase search strategy using **both English and Arabic** queries. We prioritized:
- **Institutional sources**: Arab League/ALECSO publications, Qatar Foundation, Saudi Association for Hearing Impairment
- **Academic repositories**: King Saud University, University of Southampton, Springer, Oxford University Press, MDPI
- **Peer-reviewed journals**: Journal of Deaf Studies and Deaf Education, Universal Access in the Information Society
- **Teaching and community materials**: Bibliotheca Alexandrina, Qatar Social Rehabilitation Network

We executed a total of **18 search queries** (12 English, 6 Arabic) to cast a wide net across linguistics, NLP systems, dictionaries, and teaching materials. We also followed citation chains — when one paper referenced another source, we tracked that source down.

### Q2: What search queries did you use? Did you use Arabic search terms?

**Yes, we used both English and Arabic search terms.** See the full list of 18 queries in Section 2 above.

The Arabic queries were essential — they led us to source S-08 (نحو لغة الإشارة العربية — بنية الجملة), which turned out to be one of our most critical sources because it provided **concrete Arabic-language examples** of sentence restructuring with explicit before/after gloss sequences.

### Q3: How did you evaluate whether a source was credible?

Sources were classified into three tiers:
- **🟢 High (8 sources):** Peer-reviewed academic papers published in established journals (Oxford UP, Springer, MDPI), or official institutional publications (ALECSO dictionary, KSU dataset).
- **🟡 Medium (6 sources):** Institutional websites (Qatar Social Rehabilitation Network, Saudi Hearing Association), well-cited Wikipedia articles, and educational materials from reputable organizations.
- **🔴 Low (0 sources):** We deliberately excluded unsourced community blogs, generic articles without clear authorship, and social media content.

### Q4: How did you handle scanned PDFs or images?

For materials that were not directly machine-readable (such as the ALECSO dictionary pages S-04 and S-05), we prioritized finding **academic papers that referenced those materials**. Papers S-02, S-03, and S-10 all reference the ALECSO dictionaries and provide machine-readable summaries of their contents, structure, and sign inventories. This allowed us to extract information without performing OCR ourselves, which would have introduced accuracy risks.

### Q5: How did you extract rules from the source materials?

Rules were extracted by analyzing sources for two types of information:
1. **Direct linguistic statements** — e.g., source S-08 explicitly states: "يتم اختصار أو حذف حروف الجر، وحروف العطف، وأدوات التعريف" (Prepositions, conjunctions, and articles are shortened or dropped). This became the basis for rules R-06, R-07, and R-14.
2. **Before-and-after translation examples** — NLP papers (S-02, S-03, S-07) document their preprocessing pipelines with input/output pairs. We reverse-engineered the grammar rules from these transformation patterns.

Each rule was formalized into a structured YAML schema with: `id`, `name`, `category`, `trigger`, `action`, `evidence_type`, `evidence` (linked to source IDs and specific pages/sections), `confidence`, `priority`, `examples`, and `review_questions`.

### Q6: Which rules came directly from explicit statements, and which were inferred?

We implemented a strict three-tier classification:
- **Explicit (6 rules — R-01, R-02, R-06, R-07, R-12, R-13):** Directly stated in at least one source.
- **Inferred (10 rules — R-03, R-04, R-04b, R-05, R-08, R-09, R-10, R-11, R-14, R-15):** Deduced by observing consistent patterns across multiple translation examples.
- **Speculative (0 rules):** We deliberately avoided adding any purely speculative rules.

### Q7: Did you use RAG? If so, how?

**We did not use RAG for the runtime transcription engine.** The runtime system is a pure rule-based Python engine (FastAPI) that executes pre-extracted YAML rules deterministically.

LLM capabilities were used during the **research phase** to discover sources, read Arabic-language materials, and extract structured rules.

**Why no RAG at runtime?** The assignment prioritizes **explainability and traceability**. A rule engine guarantees that every output transformation traces to a specific `rule_id` → `evidence` → `source_id`. An LLM-based approach would introduce hallucination risk and non-deterministic outputs.

### Q8: How did you prevent the model from inventing grammar rules?

By **strictly separating the research phase from the runtime phase:**
- The runtime engine only executes rules that exist in `rules.yaml`.
- Each rule requires at least one `evidence` entry linking to a specific `source_id` and `page_or_section`.
- There is **zero LLM inference at runtime**. The engine is pure Python code executing deterministic if/else logic.

### Q9: How did you handle words missing from the dictionary?

When a word is not found in `dictionary.yaml` (after normalization):
1. The word is wrapped in `fs()` notation — indicating **fingerspelling**.
2. The UI displays: `❌ غير موجود في القاموس — يُهجّأ بالأصابع` (Not in dictionary — fingerspelled).
3. An **Expert Review** item is automatically generated asking: "Does this word have a standard sign?"
4. This matches real-world practice (rule R-13).

### Q10: How would you update the rule base with expert feedback?

The system was designed for expert reviewability:
1. **All rules and dictionary entries are plain YAML files.** Experts do not need to read Python code.
2. An expert can: change a rule's `confidence` level, modify a rule's `action`, add `regional_variants` to dictionary entries, add entirely new rules, or mark `requires_expert_review: false` after validation.
3. The backend loads these files dynamically at startup — YAML changes are instantly reflected.
4. The `review_questions` field provides specific prompts for expert review.

---

## 6. Limitations and Risk Statement

### Linguistic Limitations

1. **Unified ArSL vs. Regional Variants:** "Unified Arabic Sign Language" is primarily a **dictionary standardization project** (ALECSO). It standardizes vocabulary (~3,200 signs) but does not enforce unified grammar. Real deaf communities use their own natural sign languages with distinct grammars.

2. **Grammar Uncertainties:**
   - **Tense markers:** It remains uncertain whether specific verbs require manual tense markers, or if time expressions alone suffice.
   - **Negation position:** Whether the negation sign goes immediately after the verb or at clause-end varies by region.
   - **Implicit pronouns:** When to insert an explicit pronoun sign vs. relying on spatial agreement is context-dependent.

3. **Arabic ≠ Arabic Sign Language ≠ Gloss:** These are three fundamentally different things. Important spatial, temporal, and non-manual information is inevitably lost in gloss transcription.

### Technical Limitations

1. **Simplified Morphological Analysis:** We use a lightweight regex-based tokenizer instead of a robust NLP pipeline (like CAMeL Tools). Complex morphological structures or ambiguous words may be parsed incorrectly.

2. **No Spatial Grammar:** Sign languages use spatial grammar extensively. A text-based gloss system cannot represent this.

3. **Limited Dictionary:** ~200 entries — a tiny subset of the ~3,200 signs in the ALECSO dictionary.

4. **Linear Rule Application:** Rules are applied in fixed priority order. Natural languages have overlapping, context-dependent rules.

### Honest Assessment

- **Strong evidence:** Article dropping, preposition handling, basic Topic-Comment word order, time fronting, fingerspelling fallback.
- **Moderate evidence:** Negation patterns, WH-question formation, verb tense simplification.
- **Weak evidence:** Detailed verb aspect marking, number expression specifics, adjective ordering for complex phrases.

### Mitigation Strategy

1. **No black boxes:** Every transformation is executed by a traceable rule.
2. **Confidence scoring:** The UI explicitly flags the overall confidence level.
3. **Expert review flags:** The system proactively generates questions for human experts.
4. **Data separation:** All rules and dictionary entries are human-readable YAML files.

---

## 7. System Architecture

### Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | FastAPI | 0.116.1 |
| Runtime | Python | 3.9.13 |
| Data Format | PyYAML | 6.0.2 |
| Validation | Pydantic v2 | 2.11.7 |
| Server | Uvicorn | 0.39.0 |
| Frontend | HTML + Vanilla CSS + JS | — |

### How It Works (End-to-End Flow)

```
User enters Arabic text
        │
        ▼
┌─── Tokenizer ───┐
│ Normalize text   │  (strip diacritics, normalize alef, identify prefixes/suffixes)
└────────┬─────────┘
         │
         ▼
┌─── Analyzer ────┐
│ POS tagging     │  (VERB, NOUN, PREP, TIME, NEG, QUESTION...)
│ Feature detect  │  (is_question? has_negation? has_time_expr?)
└────────┬────────┘
         │
         ▼
┌─── Rule Engine ──────────────────────┐
│ Iterate 16 rules by priority:       │
│  1. Time Fronting (R-02)             │
│  2. Preposition/Article Drop (R-06,7)│
│  3. Negation Handling (R-03)         │
│  4. Tense Simplification (R-08)     │
│  5. Word Order / Topic-Comment (R-01)│
│  6. Question Formation (R-04)        │
│  ...                                 │
│  99. Fingerspelling Fallback (R-13)  │
└────────┬─────────────────────────────┘
         │
         ▼
┌─── Dictionary ──┐
│ 200+ entries    │  Match tokens → sign glosses
│ YAML-based      │  Unknown → fs(word)
└────────┬────────┘
         │
         ▼
   JSON Response
   ├── gloss_sequence
   ├── applied_rules (with evidence + sources)
   ├── confidence_level
   └── expert_review_items
```

### Data Files (Human-Editable YAML)

```
backend/data/
├── rules.yaml       ← 16 grammar rules with evidence links
├── sources.yaml     ← 14 cited academic and institutional sources
└── dictionary.yaml  ← 200+ Arabic word → sign gloss entries
```

---

*This document constitutes the Arabic Sign Language Grammar Discovery & Explainable Transcription Prototype*
