const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  versions: {
    node: process.versions.node,
    chrome: process.versions.chrome,
    electron: process.versions.electron
  },
  platform: process.platform,

  app: {
    relaunch: () => ipcRenderer.invoke('app-relaunch')
  },

  // 应用内自动更新桥接：页脚「新版本」徽章点击时调用，
  // 在桌面端直接触发静默下载 + 重启，而不是打开浏览器 releases 页。
  updates: {
    checkAndDownload: () => ipcRenderer.invoke('app:check-for-updates'),
    install: () => ipcRenderer.invoke('app:install-update'),
  },

  logs: {
    getDirectory: () => ipcRenderer.invoke('get-logs-directory'),
    listFiles: () => ipcRenderer.invoke('list-log-files'),
    readFile: (filename) => ipcRenderer.invoke('read-log-file', filename),
    openFolder: () => ipcRenderer.invoke('open-logs-folder')
  }
});
