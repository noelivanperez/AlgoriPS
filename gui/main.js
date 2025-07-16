const fs = require('fs');
const path = require('path');

// Attempt to use the compiled JavaScript build first. This avoids
// requiring ts-node during runtime when dependencies are not installed.
const compiled = path.join(__dirname, 'dist', 'electron.js');

if (fs.existsSync(compiled)) {
  require(compiled);
} else {
  // Fallback to executing the TypeScript source via ts-node.
  require('ts-node/register');
  require('./electron.ts');
}
