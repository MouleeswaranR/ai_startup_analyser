const API = window.location.origin.includes('localhost') ? 'http://localhost:8000' : window.location.origin;
let jobId = null, poll = null, data = {};

// Fill example
function fill(btn) {
    document.getElementById('idea').value = 'Create a startup that offers ' + btn.textContent;
    document.getElementById('idea').focus();
}

// Launch
async function launch() {
    const idea = document.getElementById('idea').value.trim();
    if (!idea) { toast('Type your startup idea first', 'err'); return; }

    const btn = document.getElementById('go');
    btn.disabled = true; btn.textContent = '⏳ Launching...';
    updateStatus('Starting job...', 'running');

    try {
        const health = await getHealth();
        if (!health || health.status !== 'ok') {
            throw new Error('API health check failed');
        }

        const selectedModel = document.getElementById('model').value;

        const r = await fetch(API + '/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ startup_idea: idea, model: selectedModel })
        });

        if (!r.ok) {
            const err = await r.json().catch(() => ({}));
            throw new Error(err.detail || 'Failed to create job');
        }

        const d = await r.json();
        jobId = d.job_id;
        document.getElementById('job-id').textContent = jobId;
        document.getElementById('job-idea').textContent = idea;
        toast('Agents started! Job: ' + jobId, 'ok');
        showProgress();
        startPoll();
    } catch (e) {
        toast('Unable to start job: ' + e.message, 'err');
        updateStatus('Unable to connect to API', 'err');
        btn.disabled = false; btn.textContent = '🚀 Launch Company';
    }
}

// Polling
function startPoll() {
    const timers = [0, 2000, 20000, 40000, 60000, 80000];
    timers.forEach((t, i) => {
        setTimeout(() => { if (i < 5) setStep(i, Math.min(15 + i * 18, 90)); }, t);
    });

    poll = setInterval(async () => {
        try {
            const r = await fetch(API + '/api/status/' + jobId);
            const s = await r.json();
            updateStatus(`Job ${jobId} — ${capitalize(s.status)}`, s.status === 'failed' ? 'err' : 'running');
            if (s.status === 'completed') { clearInterval(poll); await getResults(); }
            if (s.status === 'failed') { clearInterval(poll); toast('Failed: ' + (s.error || '?'), 'err'); resetBtn(); }
        } catch (e) {
            console.error(e);
        }
    }, 2500);
}

async function getResults() {
    const r = await fetch(API + '/api/results/' + jobId);
    const d = await r.json();
    if (d.status && d.status !== 'completed') {
        updateStatus(`Waiting for completion: ${d.status}`, 'running');
        return;
    }
    if (d.results) { data = d.results; render(data); }
}

async function getHealth() {
    try {
        const r = await fetch(API + '/api/health');
        if (!r.ok) return null;
        return await r.json();
    } catch (e) {
        return null;
    }
}

function updateStatus(text, variant) {
    const chip = document.getElementById('status-chip');
    chip.textContent = text;
    chip.className = 'status-chip';
    if (variant === 'err') chip.classList.add('err');
}

function capitalize(text) {
    return text ? text.charAt(0).toUpperCase() + text.slice(1) : text;
}

// Progress UI
function showProgress() {
    document.getElementById('input-card').style.display = 'none';
    document.getElementById('progress').classList.add('show');
    document.getElementById('results-section').classList.remove('show');
    setDots('idle');
}

function setStep(i, pct) {
    document.getElementById('bar').style.width = pct + '%';
    document.getElementById('pct').textContent = pct + '%';
    const names = ['ceo', 'research', 'dev', 'mkt', 'support'];
    for (let j = 0; j < 5; j++) {
        const el = document.getElementById('s' + j);
        const num = el.querySelector('.step-num');
        if (j < i) { el.className = 'step done'; num.textContent = '✓'; setDot(names[j], 'done'); }
        else if (j === i) { el.className = 'step active'; num.textContent = j + 1; setDot(names[j], 'active'); }
        else { el.className = 'step'; num.textContent = j + 1; }
    }
}

function setDot(name, cls) { document.getElementById('d-' + name).className = 'dot ' + cls; }
function setDots(cls) { ['ceo','research','dev','mkt','support'].forEach(n => setDot(n, cls)); }

// Render results
function render(d) {
    document.getElementById('bar').style.width = '100%';
    document.getElementById('pct').textContent = '100%';
    for (let i = 0; i < 5; i++) {
        const el = document.getElementById('s' + i);
        el.className = 'step done';
        el.querySelector('.step-num').textContent = '✓';
    }
    setDots('done');
    setTimeout(() => {
        document.getElementById('progress').classList.remove('show');
        document.getElementById('results-section').classList.add('show');
    }, 800);

    const map = {
        ceo_strategy: 'ceo', market_research: 'research',
        product_development: 'dev', marketing_plan: 'mkt', customer_support: 'support'
    };
    for (const [k, v] of Object.entries(map)) {
        const el = document.getElementById('c-' + v);
        if (el) el.innerHTML = md(d[k] || 'No data.');
    }
    if (d.full_report) document.getElementById('full-report').innerHTML = md(d.full_report);
    toast('All 5 agents finished!', 'ok');
}

// Tabs
function tab(name, btn) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('p-' + name).classList.add('active');
}

// Download
function dl(key) {
    const el = document.getElementById('c-' + key);
    if (!el || el.textContent === '—') { toast('No content yet', 'info'); return; }
    const names = { ceo: 'ceo_strategy', research: 'market_research', dev: 'product_development', mkt: 'marketing_plan', support: 'customer_support' };
    const blob = new Blob([el.innerText], { type: 'text/markdown' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = (names[key] || key) + '.md';
    a.click();
    toast('Downloaded!', 'ok');
}

// Full report toggle
function toggleFull() {
    document.getElementById('full-report').classList.toggle('show');
}

// Reset
function reset() {
    jobId = null; data = {};
    if (poll) clearInterval(poll);
    document.getElementById('results-section').classList.remove('show');
    document.getElementById('progress').classList.remove('show');
    document.getElementById('input-card').style.display = '';
    document.getElementById('idea').value = '';
    setDots('idle');
    resetBtn();
    document.getElementById('bar').style.width = '0%';
    document.getElementById('pct').textContent = '0%';
    for (let i = 0; i < 5; i++) {
        const el = document.getElementById('s' + i);
        el.className = 'step';
        el.querySelector('.step-num').textContent = i + 1;
    }
    ['ceo','research','dev','mkt','support'].forEach(k => {
        document.getElementById('c-' + k).textContent = '—';
    });
    document.getElementById('full-report').innerHTML = '';
    document.getElementById('full-report').classList.remove('show');
}

function resetBtn() {
    const btn = document.getElementById('go');
    btn.disabled = false; btn.textContent = '🚀 Launch Company';
}

async function loadHistory() {
    try {
        const r = await fetch(API + '/api/history');
        const data = await r.json();
        const body = document.getElementById('history-body');
        if (!data.runs || data.runs.length === 0) {
            body.innerHTML = '<div class="history-empty">No history yet. Run a startup idea to populate recent jobs.</div>';
            return;
        }

        const items = data.runs.slice(0, 5).map(run => {
            const statusClass = run.status === 'completed' ? 'completed' : run.status === 'failed' ? 'failed' : 'running';
            return `
                <div class="history-item">
                    <div>
                        <strong>${run.startup_idea}</strong>
                        <span>${new Date(run.started_at).toLocaleString()}</span>
                    </div>
                    <div>
                        <span class="status-pill ${statusClass}">${run.status}</span>
                        <button class="btn btn-ghost btn-sm" onclick="openHistory('${run.job_id}')">View</button>
                    </div>
                </div>
            `;
        }).join('');

        body.innerHTML = items;
    } catch (e) {
        console.error(e);
        toast('Unable to load history', 'err');
    }
}

function openHistory(runId) {
    if (!runId) return;
    jobId = runId;
    document.getElementById('input-card').style.display = 'none';
    document.getElementById('progress').classList.remove('show');
    document.getElementById('results-section').classList.add('show');
    document.getElementById('job-id').textContent = runId;
    fetch(API + '/api/results/' + runId)
        .then(r => r.json())
        .then(d => {
            if (d.results) {
                document.getElementById('job-idea').textContent = d.startup_idea || '—';
                data = d.results;
                render(data);
            } else {
                toast('Selected job has no results yet', 'info');
            }
        })
        .catch(() => toast('Unable to load job', 'err'));
}

// Markdown renderer with table support
function md(t) {
    if (!t) return '';

    // Parse tables FIRST (before escaping)
    const lines = t.split('\n');
    let html = '';
    let inTable = false;
    let tableRows = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // Detect table row: starts and ends with | or has | separators
        if (line.match(/^\|(.+)\|$/)) {
            // Skip separator rows like | --- | --- |
            if (line.match(/^\|[\s\-:]+\|$/)) continue;
            tableRows.push(line);
            inTable = true;
        } else {
            // If we were in a table, flush it
            if (inTable && tableRows.length > 0) {
                html += buildTable(tableRows);
                tableRows = [];
                inTable = false;
            }
            // Process regular line
            html += processLine(line) + '\n';
        }
    }
    // Flush any remaining table
    if (tableRows.length > 0) html += buildTable(tableRows);

    return html;
}

function buildTable(rows) {
    let h = '<table class="md-table"><thead><tr>';
    // First row = header
    const headerCells = rows[0].split('|').filter(c => c.trim());
    headerCells.forEach(c => { h += '<th>' + esc(c.trim()) + '</th>'; });
    h += '</tr></thead><tbody>';
    // Remaining rows = body
    for (let i = 1; i < rows.length; i++) {
        h += '<tr>';
        const cells = rows[i].split('|').filter(c => c.trim());
        cells.forEach(c => { h += '<td>' + esc(c.trim()) + '</td>'; });
        h += '</tr>';
    }
    h += '</tbody></table>';
    return h;
}

function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function processLine(line) {
    let s = esc(line);
    // Headers
    s = s.replace(/^### (.+)$/, '<h3>$1</h3>');
    s = s.replace(/^## (.+)$/, '<h2>$1</h2>');
    s = s.replace(/^# (.+)$/, '<h1>$1</h1>');
    // Bold & italic
    s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    s = s.replace(/\*(.+?)\*/g, '<em>$1</em>');
    // Inline code
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    // List items
    s = s.replace(/^- (.+)$/, '<li>$1</li>');
    s = s.replace(/^\d+\. (.+)$/, '<li>$1</li>');
    // Horizontal rule
    s = s.replace(/^---$/, '<hr style="border:none;border-top:1px solid #e5e7eb;margin:12px 0">');
    // Empty line = paragraph break
    if (s === '') s = '<br>';
    return s;
}

// Toast
function toast(msg, type) {
    const box = document.getElementById('toasts');
    const el = document.createElement('div');
    el.className = 'toast ' + (type || 'info');
    el.textContent = msg;
    box.appendChild(el);
    setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, 3500);
}

// Ctrl+Enter
document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 'Enter') launch();
});
