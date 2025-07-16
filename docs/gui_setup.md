# GUI Setup

1. Install Node.js and npm.
2. Navigate to the `gui` folder and run `npm install` (requires internet).

   This installs all dependencies including **ts-node**, which is required for
   starting Electron from the TypeScript entry point.

3. Launch development mode with `npm run start`. The start script first compiles
   the TypeScript sources, generating `dist/index.js`, and then launches
   Electron.
4. Build the desktop app with `npm run make`.

