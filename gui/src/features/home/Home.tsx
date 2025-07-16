import React from 'react';
import { useAppStore } from '../../store';

const Home: React.FC = () => {
  const setProjectPath = useAppStore(state => state.setProjectPath);

  const onSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    setProjectPath(e.target.value);
  };

  return (
    <div>
      <h2>Select Project</h2>
      <input type="text" onChange={onSelect} placeholder="/path/to/project" />
    </div>
  );
};

export default Home;
