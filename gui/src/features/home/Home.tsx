import React from 'react';
import { useAppStore } from '../../store';

const Home: React.FC = () => {
  const setProjectPath = useAppStore(state => state.setProjectPath);

  const onSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    setProjectPath(e.target.value);
  };

  return (
    <div className="p-6 max-w-lg mx-auto bg-surface rounded-xl shadow space-y-4">
      <h2 className="text-xl font-semibold">Choose project directory</h2>
      <label htmlFor="project-path" className="sr-only">Project path</label>
      <input
        id="project-path"
        type="text"
        onChange={onSelect}
        placeholder="/path/to/project"
        className="border rounded p-2 w-full"
      />
    </div>
  );
};

export default Home;

