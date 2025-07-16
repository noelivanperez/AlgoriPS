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
    <form onSubmit={onSubmit}>
      <input name="example" onChange={onChange} value={(local as any).example || ''} />
      <button type="submit">Save</button>
    </form>
  );
};

export default SettingsPage;
