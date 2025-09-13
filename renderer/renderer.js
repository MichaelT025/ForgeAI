const $ = (id) => document.getElementById(id);

// Elements
const promptEl = $('prompt');
const planEl = $('plan');
const codeEl = $('code');
const warnEl = $('warnings');
const logsEl = $('logs');
const statusDot = $('statusDot');
const statusText = $('statusText');
const runSpinner = $('runSpinner');
const planBadges = $('planBadges');

// Helpers
function setStatus(mode) {
  // mode: 'idle' | 'preview' | 'running' | 'done' | 'error'
  const dot = statusDot.classList;
  dot.remove('ok','run');
  switch (mode) {
    case 'preview':
      statusText.textContent = 'Preview ready';
      dot.add('ok');
      break;
    case 'running':
      statusText.textContent = 'Running macro…';
      dot.add('run');
      break;
    case 'done':
      statusText.textContent = 'Done';
      dot.add('ok');
      break;
    case 'error':
      statusText.textContent = 'Error';
      break;
    default:
      statusText.textContent = 'Idle';
  }
}

function clearLogs(){ logsEl.textContent = ''; }
function log(line){ logsEl.textContent += (line || '') + '\n'; logsEl.scrollTop = logsEl.scrollHeight; }

async function doPreview() {
  const res = await window.AISW.previewFromPrompt(promptEl.value);
  planEl.textContent = res.plan || '(no plan)';
  codeEl.textContent = res.vbs || '(no code)';
  warnEl.textContent = (res.warnings && res.warnings.length) ? res.warnings.join('\n') : '(none)';

  // Tiny badges extracted from plan
  planBadges.innerHTML = '';
  const plane = (res.plan || '').match(/Plane:\s*([a-z]+)/i)?.[1];
  const size = (res.plan || '').match(/Box:\s*([^\n]+)/i)?.[1];
  const fillet = (res.plan || '').match(/Fillet:\s*([^\n]+)/i)?.[1];
  const parts = [plane && `Plane: ${plane}`, size && `Box: ${size}`, fillet && `Fillet: ${fillet}`].filter(Boolean);
  if (parts.length) planBadges.textContent = parts.join(' • ');

  setStatus('preview');
}

async function doRun() {
  setStatus('running'); runSpinner.style.display = '';
  clearLogs();
  // preview first so the right code is shown
  await doPreview();
  await window.AISW.runFromPrompt(promptEl.value);
}

$('previewBtn').addEventListener('click', doPreview);
$('runBtn').addEventListener('click', doRun);

// Copy buttons
document.querySelectorAll('.copybtn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const target = btn.getAttribute('data-copy-target');
    const el = $(target);
    try {
      await navigator.clipboard.writeText(el.textContent || '');
      btn.textContent = 'Copied';
      setTimeout(() => btn.textContent = 'Copy', 900);
    } catch (e) {
      btn.textContent = 'Failed';
      setTimeout(() => btn.textContent = 'Copy', 900);
    }
  });
});

// Log streaming from main
window.AISW.onLog(msg => { log(msg); });
window.AISW.onError(msg => { log('[ERROR] ' + msg); setStatus('error'); });
window.AISW.onDone(_ => { setStatus('done'); runSpinner.style.display = 'none'; });

// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); doPreview(); }
  if (e.ctrlKey && e.shiftKey && e.key === 'Enter') { e.preventDefault(); doRun(); }
});

// Seed example prompt on first load
if (!promptEl.value) {
  promptEl.value = 'Create a 120x80x25 mm box on front plane. Add 8 mm fillet to all edges.';
}
setStatus('idle');
