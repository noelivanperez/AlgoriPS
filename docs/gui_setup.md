# GUI Setup

1. Install Node.js and npm.
2. Navigate to `gui` folder and run the following commands (requires internet):

   ```
   npm install
   npx tsc    # generates dist/index.js
   cp public/index.html index.html  # or modify electron.ts accordingly
   ```

   This installs all dependencies including **ts-node**, which is required for starting
   Electron from the TypeScript entry point.
3. Launch development mode with `npm run start`.
4. Build the desktop app with `npm run make`.

