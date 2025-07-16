import React, { useEffect, useState } from 'react';
import { listPlugins, installPlugin, uninstallPlugin } from '../../utils/api';

interface PluginInfo {
  name: string;
  version: string;
  active: boolean;
}

const Plugins: React.FC = () => {
  const [plugins, setPlugins] = useState<PluginInfo[]>([]);
  const [path, setPath] = useState('');

  const fetchPlugins = async () => {
    const data = await listPlugins();
    setPlugins(data);
  };

  useEffect(() => {
    fetchPlugins();
  }, []);

  const onInstall = async () => {
    await installPlugin(path);
    setPath('');
    fetchPlugins();
  };

  const onUninstall = async (name: string) => {
    await uninstallPlugin(name);
    fetchPlugins();
  };

  return (
    <div>
      <h2>Plugins</h2>
      <div>
        <input
          value={path}
          onChange={e => setPath(e.target.value)}
          placeholder="plugin path"
        />
        <button onClick={onInstall}>Install</button>
      </div>
      <ul>
        {plugins.map(p => (
          <li key={p.name}>
            {p.name} {p.version}{' '}
            <button onClick={() => onUninstall(p.name)}>Uninstall</button>{' '}
            <button onClick={() => window.open(`/plugins/${p.name}/README.md`)}>
              View docs
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Plugins;
