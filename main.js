const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { generateVbsFromPrompt } = require('./codegen');
const { runVbs } = require('./runner');

let win;

async function createWindow() {
  win = new BrowserWindow({
    width: 980,
    height: 700,
    webPreferences: {
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    }
  });
  await win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

/** Preview: prompt -> show plan + code (no execution) */
ipcMain.handle('preview:fromPrompt', async (_evt, promptText) => {
  const { plan, vbs, warnings } = generateVbsFromPrompt(promptText);
  return { plan, vbs, warnings };
});

/** Run: prompt -> code -> execute with cscript -> live logs */
ipcMain.handle('run:fromPrompt', async (evt, promptText) => {
  const { plan, vbs, warnings } = generateVbsFromPrompt(promptText);
  // stream logs back to renderer
  return await runVbs(vbs, (line) => {
    win.webContents.send('runner:log', line);
  }, (err) => {
    win.webContents.send('runner:error', String(err));
  }, () => {
    win.webContents.send('runner:done', 'Done');
  });
});
