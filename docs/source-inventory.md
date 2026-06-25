# ArSL Transcriber — Source Inventory

> **Generated**: 2026-06-25 | **Phase**: 1 (Source Discovery) | **Total Sources**: 14 (6 Arabic, 8 English/Both)

---

## Summary

| Metric | Count |
|--------|-------|
| Total sources | 14 |
| High credibility | 8 |
| Medium credibility | 6 |
| Low credibility | 0 |
| Arabic-language sources | 5 |
| English-language sources | 8 |
| Bilingual sources | 1 |
| Academic/peer-reviewed | 7 |
| Dictionary resources | 3 |
| Teaching materials | 2 |
| Grammar-focused | 2 |

---

## Search Methodology

### English Queries Executed
1. `"Unified Arabic Sign Language" grammar rules`
2. `"Arabic Sign Language" sentence structure gloss`
3. `ArSL word order syntax morphology`
4. `"Arabic Sign Language" dictionary PDF`
5. `"Arabic Sign Language" linguistic analysis`
6. `Arab League ALECSO sign language unified dictionary`
7. `Saudi Egyptian Jordanian deaf association sign language research`
8. `King Saud University Arabic sign language research`
9. `Almasoud Alwohaibi "Arabic text to Arabic sign language" rule-based translation`
10. `Almohimeed Al-Khalifa Wald "Arabic text to ArSL gloss" Southampton`
11. `Luqman Mahmoud "Automatic translation Arabic text Arabic sign language"`
12. `Arabic Sign Language text to gloss translation rules morphological analysis`

### Arabic Queries Executed
1. `قواعد لغة الإشارة العربية الموحدة`
2. `ترتيب الجملة في لغة الإشارة العربية`
3. `معجم لغة الإشارة العربية الموحدة`
4. `تعليم لغة الإشارة للصم العرب`
5. `نحو لغة الإشارة العربية بنية الجملة`
6. `"القاموس الإشاري العربي" PDF تحميل جامعة الدول العربية`

---

## Source Inventory Table

| ID | Title | Lang | Type | Credibility | Year |
|----|-------|------|------|-------------|------|
| S-01 | Arabic Sign Language: A Perspective | EN | Academic | 🟢 High | 2005 |
| S-02 | An Arabic Text-to-Arabic Sign Language Translation System | EN | Academic | 🟢 High | 2011 |
| S-03 | Automatic translation of Arabic text to Arabic sign language | EN | Academic | 🟢 High | 2019 |
| S-04 | القاموس الإشاري العربي للصم — الجزء الأول | AR | Dictionary | 🟢 High | 2001 |
| S-05 | القاموس الإشاري العربي للصم — الجزء الثاني | AR | Dictionary | 🟢 High | 2007 |
| S-06 | Arab Sign-Language Family — Wikipedia | EN | Grammar | 🟡 Medium | 2024 |
| S-07 | Semantic Machine Translation: Arabic Text to ArSL | EN | Academic | 🟢 High | 2011 |
| S-08 | نحو لغة الإشارة العربية — بنية الجملة | AR | Grammar | 🟡 Medium | 2023 |
| S-09 | مكتبة لغة الإشارة السعودية | AR | Dictionary | 🟡 Medium | 2022 |
| S-10 | ArSL Recognition and Translation: Survey | EN | Academic | 🟢 High | 2023 |
| S-11 | QFI — Arabic Sign Language Resources | Both | Teaching | 🟡 Medium | 2023 |
| S-12 | تعليم لغة الإشارة — قواعد وأساسيات | AR | Teaching | 🟡 Medium | 2022 |
| S-13 | ArSL Translation Using Transformer Models | EN | Academic | 🟢 High | 2023 |
| S-14 | KSU Arabic Sign Language Dataset | EN | Academic | 🟢 High | 2022 |

---

## Detailed Source Assessments

### S-01: Arabic Sign Language: A Perspective
- **Author**: Mahmoud A. Abdel-Fattah
- **Year**: 2005
- **Journal**: Journal of Deaf Studies and Deaf Education (Oxford University Press)
- **Credibility**: 🟢 **HIGH** — Peer-reviewed journal article. Foundational paper on ArSL linguistics. Most frequently cited primary source in the field.
- **Key Contributions**:
  - Contrastive analysis between spoken Arabic and various regional ArSLs
  - Documents linguistic primes: handshape, configuration, movement
  - Discusses diglossia in ArSL context (absence of MSA/colloquial split in sign)
  - Notes that ArSLs are independent languages, not codes for spoken Arabic
- **Limitations**: Overview paper, not exhaustive grammar reference. Data from 2005.
- **Rules Supported**: R-01 (word order), R-05 (pronouns), R-07 (article dropping), R-12 (non-manual markers)

### S-02: An Arabic Text-to-Arabic Sign Language Translation System
- **Author**: Abdulaziz Almohimeed, Mike Wald, Robert Damper
- **Institution**: University of Southampton
- **Year**: 2011
- **Credibility**: 🟢 **HIGH** — PhD research with ACL publication. Created bilingual Arabic-ArSL corpus. Developed complete translation pipeline.
- **Key Contributions**:
  - Documents need for reordering rules (not word-for-word)
  - Bilingual corpus creation methodology
  - Example-based + rule-based translation approach
  - Preprocessing pipeline: morphological analysis → POS tagging → reordering → gloss
- **Limitations**: Domain-specific (prayer jurisprudence). Corpus-based, not purely rule-based.
- **Rules Supported**: R-01 (word order), R-02 (time fronting), R-03 (negation), R-06 (prepositions), R-07 (articles), R-08 (tense)

### S-03: Automatic Translation of Arabic Text to Arabic Sign Language
- **Author**: H. Luqman, S. A. Mahmoud
- **Journal**: Universal Access in the Information Society (Springer)
- **Year**: 2019
- **Credibility**: 🟢 **HIGH** — Peer-reviewed Springer journal. Complete pipeline with documented preprocessing steps.
- **Key Contributions**:
  - Morphological analysis pipeline for Arabic-to-ArSL
  - Normalization rules (Alif variants, Taa Marbuta)
  - POS-based word order reordering
  - Stop word removal aligned with ArSL conventions
  - Tense marker handling
- **Limitations**: Saudi Sign Language variant. Technical paper, grammar rules embedded in implementation.
- **Rules Supported**: R-01, R-02, R-06, R-07, R-08, R-09, R-11, R-13

### S-04: القاموس الإشاري العربي للصم — الجزء الأول
- **Author**: ALECSO / Arab League
- **Year**: 2001
- **Credibility**: 🟢 **HIGH** — Official publication of Arab League Educational, Cultural and Scientific Organization. The standard reference for unified ArSL vocabulary.
- **Key Contributions**:
  - ~1600 standardized signs
  - Illustrations with handshape descriptions
  - Foundation vocabulary for unified ArSL
- **Limitations**: Vocabulary only, no grammar. Published 2001, some signs may be outdated.
- **Rules Supported**: R-07 (article dropping — words listed in lemma form), R-13 (dictionary fallback)

### S-05: القاموس الإشاري العربي للصم — الجزء الثاني
- **Author**: ALECSO / Arab League (sponsored by Qatar)
- **Year**: 2007
- **Credibility**: 🟢 **HIGH** — Continuation of official ALECSO project.
- **Key Contributions**:
  - Additional ~1600 signs (total ~3200 with Part 1)
  - Extended vocabulary coverage
- **Limitations**: Same as S-04.
- **Rules Supported**: R-07, R-13

### S-06: Arab Sign-Language Family — Wikipedia
- **Author**: Wikipedia contributors
- **Year**: 2024
- **Credibility**: 🟡 **MEDIUM** — Secondary source. Well-cited but not peer-reviewed.
- **Key Contributions**:
  - Overview of regional ArSL variants
  - CAMSA unification efforts documentation
  - Links between sign language families
- **Limitations**: Wikipedia is a secondary source. Claims need verification against primaries.
- **Rules Supported**: R-01, R-05, R-12

### S-07: Semantic Machine Translation System for Arabic Text to ArSL
- **Author**: Ameera M. Almasoud, Hend S. Al-Khalifa
- **Institution**: King Saud University
- **Year**: 2011
- **Credibility**: 🟢 **HIGH** — Conference publication. KSU institutional backing.
- **Key Contributions**:
  - Rule-based translation with domain ontology
  - Documents that word-for-word translation fails for ArSL
  - Semantic analysis requirements
- **Limitations**: Domain-specific (prayer jurisprudence). Proposed system.
- **Rules Supported**: R-01, R-06, R-07, R-08

### S-08: نحو لغة الإشارة العربية — بنية الجملة
- **Author**: QSRN (Qatar Social Rehabilitation Network)
- **Year**: 2023
- **Credibility**: 🟡 **MEDIUM** — Institutional source (Qatari government network). Provides concrete examples.
- **Key Contributions**:
  - **Critical source**: Provides explicit Arabic examples of sentence restructuring
  - Example: "ذهب الولد إلى المدرسة" → "ولد + مدرسة + ذهب"
  - Documents article/preposition dropping
  - Describes topic-comment structure
  - Documents role of facial expressions in question formation
- **Limitations**: May reflect Qatari variant. Not peer-reviewed.
- **Rules Supported**: R-01, R-02, R-03, R-04, R-06, R-09, R-12

### S-09: مكتبة لغة الإشارة السعودية
- **Author**: Saudi Association for Hearing Impairment
- **Year**: 2022
- **Credibility**: 🟡 **MEDIUM** — Official Saudi institutional platform.
- **Key Contributions**:
  - Video dictionary of Saudi Sign Language signs
  - Standardized sign vocabulary
- **Limitations**: Saudi-specific variant. Dictionary only, no grammar.
- **Rules Supported**: R-13

### S-10: ArSL Recognition and Translation: Comprehensive Survey
- **Author**: Various (MDPI survey)
- **Year**: 2023
- **Credibility**: 🟢 **HIGH** — Published in MDPI Electronics. Comprehensive survey.
- **Key Contributions**:
  - Comprehensive overview of ArSL research landscape
  - Documents ALECSO dictionary history (2000, 2006 publications)
  - Notes ~3200 signs in unified dictionary
  - Summarizes grammatical features across multiple studies
- **Limitations**: Survey paper, not primary research.
- **Rules Supported**: R-01, R-05, R-07, R-12

### S-11: QFI — Arabic Sign Language Resources
- **Author**: Qatar Foundation International
- **Year**: 2023
- **Credibility**: 🟡 **MEDIUM** — Reputable educational organization.
- **Key Contributions**:
  - Accessible infographics
  - Overview of standardization efforts
- **Limitations**: Educational material, not research-grade.
- **Rules Supported**: R-07, R-12

### S-12: تعليم لغة الإشارة — قواعد وأساسيات
- **Author**: Bibliotheca Alexandrina
- **Year**: 2022
- **Credibility**: 🟡 **MEDIUM** — Major Egyptian cultural institution.
- **Key Contributions**:
  - Fundamental sign language parameters (handshape, location, movement)
  - Basic sentence construction principles
- **Limitations**: Teaching-focused. Egyptian variant. Limited syntax coverage.
- **Rules Supported**: R-01, R-09, R-12

### S-13: ArSL Translation Using Transformer Models with Data Augmentation
- **Author**: MADA Center, Qatar
- **Year**: 2023
- **Credibility**: 🟢 **HIGH** — MADA is Qatar's national assistive technology center.
- **Key Contributions**:
  - AraT5 transformer model for ArSL translation
  - Documented preprocessing rules
  - Data augmentation techniques for low-resource ArSL
- **Limitations**: ML-focused. Grammar rules are implicit in training data.
- **Rules Supported**: R-01, R-02, R-06, R-07, R-08

### S-14: KSU Arabic Sign Language Dataset
- **Author**: King Saud University
- **Year**: 2022
- **Credibility**: 🟢 **HIGH** — Leading Saudi university. Published on NIH/PubMed.
- **Key Contributions**:
  - KSU-SSL dataset with thousands of video samples
  - Benchmark for ArSL recognition
- **Limitations**: Recognition-focused (sign-to-text), not translation (text-to-sign).
- **Rules Supported**: R-13

---

## Key Findings from Source Discovery

### 1. There Is No Single "Arabic Sign Language"
Multiple sources (S-01, S-06, S-10) confirm that ArSL is a **family of languages**, not a single language. Regional variants (Egyptian, Saudi, Jordanian, Levantine, etc.) have their own grammars.

### 2. The "Unified" Project Is Vocabulary-Only
The ALECSO unified dictionary (S-04, S-05) standardizes vocabulary (~3200 signs) but does **not** establish unified grammar rules. This is a critical limitation for our project.

### 3. Common Grammatical Patterns Emerge
Despite regional variation, multiple sources agree on these cross-cutting patterns:
- **Topic-Comment structure** (subject/topic first, then comment)
- **Time fronting** (temporal expressions placed first)
- **Article dropping** (الـ definite article is removed)
- **Preposition simplification** (many prepositions dropped or simplified)
- **Non-manual markers** for questions and negation
- **SVO or SOV preferred** over Arabic's typical VSO

### 4. Research Gap
Sources S-01 and S-10 note a significant **scarcity of exhaustive syntactic studies** for ArSL. Most grammar knowledge comes from:
- Translation system implementations (S-02, S-03, S-07)
- Teaching materials (S-08, S-12)
- General sign language typology applied to ArSL

### 5. Honest Assessment of Our Evidence Base
- **Strong evidence**: Article dropping, preposition handling, basic word order
- **Moderate evidence**: Time fronting, negation patterns, question formation
- **Weak evidence**: Detailed verb aspect marking, number expression rules, adjective placement specifics

---

## Source Distribution

```
Academic (7): S-01, S-02, S-03, S-07, S-10, S-13, S-14
Dictionary (3): S-04, S-05, S-09
Grammar (2): S-06, S-08
Teaching (2): S-11, S-12
```

---

*End of source inventory. See `backend/data/sources.yaml` for machine-readable version.*
