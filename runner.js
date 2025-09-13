const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

function runVbs(vbsText, onLog, onError, onDone) {
  return new Promise((resolve) => {
    const tmp = os.tmpdir();
    const file = path.join(tmp, `aisw_${Date.now()}.vbs`);
    fs.writeFileSync(file, vbsText, 'utf8');

    const cscript = 'C:\\\\Windows\\\\System32\\\\cscript.exe'; // standard path
    const child = spawn(cscript, ['//Nologo', file], { windowsHide: true });

    child.stdout.on('data', d => onLog(String(d).trim()));
    child.stderr.on('data', d => onError(String(d).trim()));
    child.on('close', (code) => {
      onDone && onDone();
      resolve({ exitCode: code });
    });
  });
}

module.exports = { runVbs };
