/**
 * ArSL Transcriber — Frontend Application
 * Handles API calls, DOM rendering, and user interaction.
 */

const API_BASE = '';  // Same origin

// ─── Core Functions ──────────────────────────────────────────────

/**
 * Insert an example sentence into the input field.
 */
function useExample(text) {
    document.getElementById('input-text').value = text;
    document.getElementById('input-text').focus();
}

/**
 * Main transcription function — called when user clicks Submit.
 */
async function transcribe() {
    const input = document.getElementById('input-text').value.trim();
    if (!input) return;

    const btn = document.getElementById('btn-transcribe');
    const btnText = btn.querySelector('.btn-text');
    const btnLoader = btn.querySelector('.btn-loader');

    // Show loading state
    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';

    try {
        const response = await fetch(`${API_BASE}/api/transcribe`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input }),
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        renderOutput(data);

    } catch (error) {
        console.error('Transcription error:', error);
        alert(`خطأ في الترجمة — Error: ${error.message}`);
    } finally {
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// ─── Rendering Functions ─────────────────────────────────────────

/**
 * Render the full transcription output.
 */
function renderOutput(data) {
    const outputSection = document.getElementById('output-section');
    outputSection.style.display = 'flex';

    // Scroll to output
    outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // 1. Gloss sequence
    renderGloss(data);

    // 2. Input echo
    renderInputEcho(data.input);

    // 3. Tokenization
    renderTokenization(data.tokenization);

    // 4. Applied rules
    renderAppliedRules(data.applied_rules);

    // 5. Dictionary status
    renderDictStatus(data.gloss_sequence);

    // 6. Evidence
    renderEvidence(data.applied_rules);

    // 7. Confidence
    renderConfidence(data.confidence);

    // 8. Expert review
    renderExpertReview(data.expert_review_items);
}

/**
 * 1. Render the gloss sequence (hero card).
 */
function renderGloss(data) {
    const display = document.getElementById('gloss-display');
    display.textContent = data.gloss_string || '—';

    const badge = document.getElementById('confidence-badge');
    const level = data.confidence?.level || 'low';
    badge.textContent = level === 'high' ? '🟢 عالي HIGH' :
                        level === 'medium' ? '🟡 متوسط MED' :
                        '🔴 منخفض LOW';
    badge.className = `confidence-badge ${level}`;
}

/**
 * 2. Render the input echo.
 */
function renderInputEcho(input) {
    document.getElementById('echo-original').textContent = input?.original || '—';
    document.getElementById('echo-normalized').textContent = input?.normalized || '—';
}

/**
 * 3. Render the tokenization table.
 */
function renderTokenization(tokens) {
    const tbody = document.getElementById('token-table-body');
    tbody.innerHTML = '';

    if (!tokens || tokens.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-state">لا توجد بيانات — No data</td></tr>';
        return;
    }

    for (const token of tokens) {
        const tr = document.createElement('tr');

        // Word
        const tdWord = document.createElement('td');
        tdWord.textContent = token.token;
        tdWord.style.fontWeight = '600';
        tr.appendChild(tdWord);

        // POS
        const tdPos = document.createElement('td');
        const posSpan = document.createElement('span');
        posSpan.className = `pos-tag ${token.pos}`;
        posSpan.textContent = token.pos;
        tdPos.appendChild(posSpan);
        tr.appendChild(tdPos);

        // Lemma
        const tdLemma = document.createElement('td');
        tdLemma.textContent = token.lemma || token.stem || '—';
        tr.appendChild(tdLemma);

        // Article
        const tdArticle = document.createElement('td');
        tdArticle.textContent = token.has_article ? 'ال ✓' : '—';
        tr.appendChild(tdArticle);

        // Prefix
        const tdPrefix = document.createElement('td');
        tdPrefix.textContent = token.prefix || '—';
        tr.appendChild(tdPrefix);

        // Features
        const tdFeatures = document.createElement('td');
        const features = token.features || {};
        if (Object.keys(features).length > 0) {
            for (const [key, value] of Object.entries(features)) {
                const tag = document.createElement('span');
                tag.className = 'feature-tag';
                tag.textContent = `${key}: ${value}`;
                tdFeatures.appendChild(tag);
            }
        } else {
            tdFeatures.textContent = '—';
        }
        tr.appendChild(tdFeatures);

        tbody.appendChild(tr);
    }
}

/**
 * 4. Render applied rules.
 */
function renderAppliedRules(rules) {
    const container = document.getElementById('applied-rules-list');

    if (!rules || rules.length === 0) {
        container.innerHTML = '<p class="empty-state">لم يتم تطبيق أي قواعد — No rules applied</p>';
        return;
    }

    container.innerHTML = '';
    for (const rule of rules) {
        const div = document.createElement('div');
        div.className = 'rule-item';
        div.innerHTML = `
            <div class="rule-header">
                <span class="rule-id">${escapeHtml(rule.rule_id)}</span>
                <span class="rule-name">${escapeHtml(rule.rule_name)}</span>
                <span class="evidence-badge ${rule.evidence_type}">${getEvidenceLabel(rule.evidence_type)}</span>
            </div>
            <p class="rule-description">${escapeHtml(rule.description)}</p>
        `;
        container.appendChild(div);
    }
}

/**
 * 5. Render dictionary status for each gloss item.
 */
function renderDictStatus(glossItems) {
    const container = document.getElementById('dict-status-list');

    if (!glossItems || glossItems.length === 0) {
        container.innerHTML = '<p class="empty-state">—</p>';
        return;
    }

    container.innerHTML = '';
    for (const item of glossItems) {
        const div = document.createElement('div');
        let statusClass = 'not-found';
        let icon = '❌';

        if (item.in_dictionary) {
            if (item.dictionary_note && item.dictionary_note.includes('غير موثّق')) {
                statusClass = 'unverified';
                icon = '⚠️';
            } else {
                statusClass = 'found';
                icon = '✅';
            }
        }

        div.className = `dict-item ${statusClass}`;
        div.innerHTML = `<span class="dict-icon">${icon}</span> <span>${escapeHtml(item.gloss)}</span>`;
        div.title = item.dictionary_note || '';
        container.appendChild(div);
    }
}

/**
 * 6. Render evidence and sources.
 */
function renderEvidence(rules) {
    const container = document.getElementById('evidence-list');

    if (!rules || rules.length === 0) {
        container.innerHTML = '<p class="empty-state">لا توجد أدلة — No evidence</p>';
        return;
    }

    // Collect all unique sources across rules
    const seenSources = new Set();
    container.innerHTML = '';

    for (const rule of rules) {
        if (!rule.sources || rule.sources.length === 0) continue;

        for (const source of rule.sources) {
            const key = `${source.source_id}-${rule.rule_id}`;
            if (seenSources.has(key)) continue;
            seenSources.add(key);

            const div = document.createElement('div');
            div.className = 'evidence-item';
            div.innerHTML = `
                <div class="source-title">${escapeHtml(rule.rule_id)}: ${escapeHtml(source.title || source.source_id)}</div>
                <p class="source-detail">${escapeHtml(source.page_or_section || '')}</p>
                <p class="source-detail">${escapeHtml(source.quote_or_summary || '')}</p>
                ${source.url ? `<a class="source-link" href="${escapeHtml(source.url)}" target="_blank" rel="noopener">${escapeHtml(source.url)}</a>` : ''}
            `;
            container.appendChild(div);
        }
    }

    if (seenSources.size === 0) {
        container.innerHTML = '<p class="empty-state">لا توجد أدلة مرتبطة — No linked evidence</p>';
    }
}

/**
 * 7. Render confidence assessment.
 */
function renderConfidence(confidence) {
    const container = document.getElementById('confidence-detail');
    const level = confidence?.level || 'low';

    container.innerHTML = `
        <div class="confidence-meter">
            <div class="confidence-fill ${level}"></div>
        </div>
        <p class="confidence-text">${escapeHtml(confidence?.explanation || '—')}</p>
    `;
}

/**
 * 8. Render expert review items.
 */
function renderExpertReview(items) {
    const container = document.getElementById('expert-review-list');

    if (!items || items.length === 0) {
        container.innerHTML = '<p class="empty-state">لا توجد عناصر تحتاج مراجعة — No items require review</p>';
        return;
    }

    container.innerHTML = '';
    for (const item of items) {
        const div = document.createElement('div');
        div.className = 'expert-item';
        div.textContent = item;
        container.appendChild(div);
    }
}

// ─── Side Panel Functions ────────────────────────────────────────

/**
 * Show a side panel (rules, sources, or dictionary).
 */
async function showPanel(type) {
    const overlay = document.getElementById('side-panel-overlay');
    const panel = document.getElementById('side-panel');
    const title = document.getElementById('panel-title');
    const body = document.getElementById('panel-body');

    overlay.style.display = 'block';
    panel.style.display = 'block';
    body.innerHTML = '<p class="loading" style="text-align:center; padding:2rem;">⏳ جارٍ التحميل... Loading...</p>';

    try {
        if (type === 'rules') {
            title.textContent = '⚙️ قاعدة القواعد — Rule Base';
            const res = await fetch(`${API_BASE}/api/rules`);
            const data = await res.json();
            renderRulesPanel(body, data.rules);
        } else if (type === 'sources') {
            title.textContent = '📚 المصادر — Sources';
            const res = await fetch(`${API_BASE}/api/sources`);
            const data = await res.json();
            renderSourcesPanel(body, data.sources);
        } else if (type === 'dictionary') {
            title.textContent = '📖 القاموس — Dictionary';
            const res = await fetch(`${API_BASE}/api/dictionary`);
            const data = await res.json();
            renderDictionaryPanel(body, data.entries);
        }
    } catch (error) {
        body.innerHTML = `<p class="empty-state">خطأ — Error: ${escapeHtml(error.message)}</p>`;
    }
}

function closePanel() {
    document.getElementById('side-panel-overlay').style.display = 'none';
    document.getElementById('side-panel').style.display = 'none';
}

function renderRulesPanel(container, rules) {
    if (!rules || rules.length === 0) {
        container.innerHTML = '<p class="empty-state">لا توجد قواعد محملة — No rules loaded</p>';
        return;
    }

    container.innerHTML = '';
    for (const rule of rules) {
        const div = document.createElement('div');
        div.className = 'panel-rule-item';
        div.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                <span class="rule-id">${escapeHtml(rule.id)}</span>
                <span class="evidence-badge ${rule.evidence_type}">${getEvidenceLabel(rule.evidence_type)}</span>
            </div>
            <h4>${escapeHtml(rule.name)}</h4>
            <p>${escapeHtml(rule.description)}</p>
            <p style="margin-top:0.4rem;"><strong>التصنيف:</strong> ${escapeHtml(rule.category)} | <strong>الثقة:</strong> ${escapeHtml(rule.confidence)} | <strong>الأولوية:</strong> ${rule.priority}</p>
            ${rule.notes ? `<p style="color:var(--accent-yellow); margin-top:0.3rem;">📝 ${escapeHtml(rule.notes)}</p>` : ''}
        `;
        container.appendChild(div);
    }
}

function renderSourcesPanel(container, sources) {
    if (!sources || sources.length === 0) {
        container.innerHTML = '<p class="empty-state">لا توجد مصادر محملة — No sources loaded</p>';
        return;
    }

    container.innerHTML = '';
    for (const source of sources) {
        const div = document.createElement('div');
        div.className = 'panel-source-item';
        div.innerHTML = `
            <h4>${escapeHtml(source.id)}: ${escapeHtml(source.title)}</h4>
            <p><strong>اللغة:</strong> ${escapeHtml(source.language)} | <strong>النوع:</strong> ${escapeHtml(source.type)} | <strong>المصداقية:</strong> ${escapeHtml(source.credibility)}</p>
            <p>${escapeHtml(source.credibility_reason || '')}</p>
            ${source.url ? `<p><a class="source-link" href="${escapeHtml(source.url)}" target="_blank">${escapeHtml(source.url)}</a></p>` : ''}
            ${source.limitations ? `<p style="color:var(--accent-yellow);">⚠️ ${escapeHtml(source.limitations)}</p>` : ''}
        `;
        container.appendChild(div);
    }
}

function renderDictionaryPanel(container, entries) {
    if (!entries || entries.length === 0) {
        container.innerHTML = '<p class="empty-state">لا توجد مدخلات — No entries loaded</p>';
        return;
    }

    // Group by category
    const grouped = {};
    for (const entry of entries) {
        const cat = entry.category || 'other';
        if (!grouped[cat]) grouped[cat] = [];
        grouped[cat].push(entry);
    }

    container.innerHTML = `<p style="color:var(--text-muted); margin-bottom:1rem;">إجمالي المدخلات: ${entries.length} — Total entries: ${entries.length}</p>`;

    for (const [category, items] of Object.entries(grouped)) {
        const section = document.createElement('div');
        section.innerHTML = `<h4 style="color:var(--accent-blue); margin:1rem 0 0.5rem; font-size:0.9rem;">${escapeHtml(category)} (${items.length})</h4>`;

        for (const item of items.slice(0, 30)) { // Show first 30 per category
            const div = document.createElement('div');
            div.className = 'panel-dict-item';
            div.innerHTML = `
                <h4>${escapeHtml(item.word)} → ${escapeHtml(item.sign_gloss)}</h4>
                <p>${item.verified ? '✅ موثّق' : '⚠️ غير موثّق'} | ${escapeHtml(item.source_id || '—')}</p>
                ${item.notes ? `<p>${escapeHtml(item.notes)}</p>` : ''}
            `;
            section.appendChild(div);
        }
        if (items.length > 30) {
            section.innerHTML += `<p class="empty-state">... و ${items.length - 30} مدخلات أخرى</p>`;
        }

        container.appendChild(section);
    }
}

// ─── UI Utilities ────────────────────────────────────────────────

/**
 * Toggle a card body's visibility.
 */
function toggleCard(bodyId) {
    const body = document.getElementById(bodyId);
    if (body) {
        body.classList.toggle('collapsed');
        // Update collapse icon
        const header = body.previousElementSibling;
        const icon = header?.querySelector('.collapse-icon');
        if (icon) {
            icon.textContent = body.classList.contains('collapsed') ? '▶' : '▼';
        }
    }
}

/**
 * Get human-readable label for evidence type.
 */
function getEvidenceLabel(type) {
    switch (type) {
        case 'explicit': return '🟢 صريح Explicit';
        case 'inferred': return '🟡 مستنتج Inferred';
        case 'speculative': return '🔴 تخميني Speculative';
        default: return type;
    }
}

/**
 * Escape HTML to prevent XSS.
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}

// ─── Keyboard Shortcut ──────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('input-text');
    if (input) {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                transcribe();
            }
        });
    }
});
