import React, { useEffect, useState } from 'react';
import { listPlugins, installPlugin, uninstallPlugin } from '../../utils/api';
import Spinner from '../../components/Spinner';

interface PluginInfo {
  name: string;
  version: string;
  active: boolean;
}

const Plugins: React.FC = () => {
  const [plugins, setPlugins] = useState<PluginInfo[]>([]);
  const [path, setPath] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchPlugins = async () => {
    const data = await listPlugins();
    setPlugins(data);
  };

  useEffect(() => {
    fetchPlugins().finally(() => setLoading(false));
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

  if (loading) return <Spinner />;
  return (
    <div className="space-y-4 max-w-3xl mx-auto">
      <h2 className="text-lg font-semibold">Plugins</h2>
      <div className="flex items-center gap-2">
        <input
          value={path}
          onChange={e => setPath(e.target.value)}
          placeholder="plugin path"
          className="border rounded p-2 flex-1"
        />
        <button className="px-4 py-2 rounded bg-primary text-white" onClick={onInstall}>Install</button>
      </div>
      <ul className="divide-y">
        {plugins.map(p => (
          <li key={p.name} className="py-1 flex items-center justify-between">
            <span>
              {p.name} {p.version}{' '}
            </span>
            <div className="flex gap-2">
              <button className="text-primary" onClick={() => onUninstall(p.name)}>Uninstall</button>{' '}
              <button className="text-primary" onClick={() => window.open(`/plugins/${p.name}/README.md`)}>
                View docs
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Plugins;
