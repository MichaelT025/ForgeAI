const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('AISW', {
  previewFromPrompt: (prompt) => ipcRenderer.invoke('preview:fromPrompt', prompt),
  runFromPrompt: (prompt) => ipcRenderer.invoke('run:fromPrompt', prompt),
  onLog: (cb) => ipcRenderer.on('runner:log', (_e, msg) => cb(msg)),
  onError: (cb) => ipcRenderer.on('runner:error', (_e, msg) => cb(msg)),
  onDone: (cb) => ipcRenderer.on('runner:done', (_e, msg) => cb(msg)),
});
