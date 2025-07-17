import { app, BrowserWindow } from 'electron';
import path from 'path';
import fs from 'fs';

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  if (process.env.NODE_ENV === 'development') {
    win.loadURL('http://localhost:3000');
  } else {
    const devPath = path.join(__dirname, 'dist', 'index.html');
    const prodPath = path.join(__dirname, '..', 'dist', 'index.html');
    const target = fs.existsSync(devPath) ? devPath : prodPath;
    win.loadFile(target);
  }
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
