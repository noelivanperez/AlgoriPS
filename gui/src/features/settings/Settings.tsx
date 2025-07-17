import React, { useState } from 'react';
import { saveSettings } from '../../utils/api';
import { useAppStore } from '../../store';

const SettingsPage: React.FC = () => {
  const current = useAppStore(state => state.settings);
  const setSettings = useAppStore(state => state.setSettings);
  const [local, setLocal] = useState(current || {});

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLocal({ ...local, [e.target.name]: e.target.value });
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await saveSettings(local);
    setSettings(local);
  };

  return (
    <form onSubmit={onSubmit} aria-label="Settings form" className="space-y-4 max-w-md mx-auto">
      <input
        name="example"
        onChange={onChange}
        value={(local as any).example || ''}
        aria-label="Example setting"
        className="border rounded p-2 w-full"
      />
      <button type="submit" className="px-4 py-2 rounded bg-primary text-white">Save</button>
    </form>
  );
};

export default SettingsPage;

