import React from 'react';
import { useAppStore } from '../../store';

const Home: React.FC = () => {
  const setProjectPath = useAppStore(state => state.setProjectPath);

  const onSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    setProjectPath(e.target.value);
  };

  return (
    <div>
      <h2>Choose project directory</h2>
      <label htmlFor="project-path" className="sr-only">Project path</label>
      <input id="project-path" type="text" onChange={onSelect} placeholder="/path/to/project" />
    </div>
  );
};

export default Home;

