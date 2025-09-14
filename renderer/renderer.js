// renderer.js — ForgeAI UI glue with status modes (Ready / Creating preview… / Forging…)
(() => {
  // ----- IPC helpers -----
  const invoke = (ch, ...args) =>
    (window.api?.invoke?.(ch, ...args)) ??
    (window.electron?.invoke?.(ch, ...args)) ??
    Promise.reject(new Error('IPC invoke not available'));

  const on = (ch, fn) => {
    if (window.api?.on) return window.api.on(ch, (_, data) => fn(data));
    if (window.electron?.on) return window.electron.on(ch, (_, data) => fn(data));
    console.warn('IPC on not available for', ch);
  };

  // ----- DOM -----
  const $ = (id) => document.getElementById(id);
  const els = {
    prompt: $('prompt'),
    plan: $('plan'),
    code: $('code'),
    planBadges: $('planBadges'),
    logs: $('logs'),
    runBtn: $('runBtn'),
    previewBtn: $('previewBtn'),
    status: $('statusText'),
    spinner: $('runSpinner'),
    statusIcon: $('statusIcon'),
    copyPlanBtn: $('copyPlanBtn'),
    copyCodeBtn: $('copyCodeBtn'),
  };

  // ----- UI utils -----
  const setStatus = (t) => { if (els.status) els.status.textContent = t; };
  const setBusy = (busy) => {
    if (els.spinner) els.spinner.classList.toggle('hidden', !busy);
    if (els.runBtn) els.runBtn.disabled = busy;
    if (els.previewBtn) els.previewBtn.disabled = busy;
  };

  // NEW: switch the little status graphic + text
  const setMode = (mode) => {
    if (!els.statusIcon) return;
    // reset icon
    els.statusIcon.className = '';
    if (mode === 'preview') {
      els.statusIcon.className = 'status-spinner';         // magenta spinner
      setStatus('Creating preview…');
    } else if (mode === 'running') {
      els.statusIcon.className = 'status-spinner run';     // ember/orange spinner
      setStatus('Forging…');
    } else {
      els.statusIcon.className = 'w-2 h-2 rounded-full bg-ember-500 animate-pulse';
      setStatus('Ready');
    }
  };

  const setPlan = (text, warnings = []) => {
    els.plan.textContent = text || '// (no plan)';
    const badge = warnings.length
      ? `⚠ ${warnings.length} warning${warnings.length > 1 ? 's' : ''}`
      : '✓ clean';
    els.planBadges.textContent = badge;
  };
  const setCode = (text) => { els.code.textContent = text || '// (no code)'; };
  const clearLogs = () => { els.logs.textContent = ''; };
  const log = (line) => {
    if (!line) return;
    els.logs.textContent += (line.endsWith('\n') ? line : line + '\n');
    els.logs.scrollTop = els.logs.scrollHeight;
  };

  // Copy buttons
  const copyFrom = (fromId, btnId) => {
    const src = $(fromId);
    if (!src) return;
    const text = src.innerText || '';
    navigator.clipboard.writeText(text).then(() => {
      const btn = $(btnId); if (!btn) return;
      const old = btn.textContent; btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = old, 900);
    }).catch(() => {});
  };
  els.copyPlanBtn?.addEventListener('click', () => copyFrom('plan', 'copyPlanBtn'));
  els.copyCodeBtn?.addEventListener('click', () => copyFrom('code', 'copyCodeBtn'));

  // ----- Actions -----
  async function doPreview() {
    const prompt = (els.prompt.value || '').trim();
    if (!prompt) return;
    setBusy(true); setMode('preview');
    try {
      const res = await invoke('preview:fromPrompt', prompt);
      setPlan(res?.plan, res?.warnings || []);
      setCode(res?.vbs);
      if (res?.warnings?.length) log('[WARN] ' + res.warnings.join('\n[WARN] '));
    } catch (err) {
      setPlan('// Preview failed', ['Preview error']);
      setCode('// ' + (err?.message || String(err)));
      log('[ERROR] ' + (err?.message || String(err)));
    } finally {
      setBusy(false); setMode('ready');
    }
  }

  async function doRun() {
    const prompt = (els.prompt.value || '').trim();
    if (!prompt) return;
    clearLogs();
    setBusy(true); setMode('running');
    log('➤ Forging macro…');

    try {
      await invoke('run:fromPrompt', prompt);
      // logs stream via runner:* events below
    } catch (err) {
      log('[ERROR] ' + (err?.message || String(err)));
      setBusy(false); setMode('ready');
    }
  }

  // ----- Wire buttons -----
  els.previewBtn?.addEventListener('click', doPreview);
  els.runBtn?.addEventListener('click', doRun);

  // Keyboard shortcuts (mirror the hints in UI)
  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); doPreview(); }
    else if (e.ctrlKey && e.shiftKey && e.key === 'Enter') { e.preventDefault(); doRun(); }
  });

  // ----- Stream logs from main -----
  on('runner:log',  (line) => log(String(line).trimEnd()));
  on('runner:error',(msg)  => log('[ERROR] ' + String(msg)));
  on('runner:done', (_msg) => { log('➤ Done'); setBusy(false); setMode('ready'); });

  // init
  setMode('ready');
})();
