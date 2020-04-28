const { ipcMain, BrowserWindow } = require('electron');


ipcMain.on('CLOSE_WINDOW', (event, args) => {
	console.log("aaaeee");
	var window = BrowserWindow.getFocusedWindow();
    window.minimize();
});