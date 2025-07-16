import React from 'react';
import { useAppStore } from '../../store';
import Card from '../../components/Card';

const Diffs: React.FC = () => {
  const diffs = useAppStore(state => state.diffs);

  return (
    <div>
      <h2>Diffs</h2>
      {diffs.map((d, idx) => (
        <Card key={idx}>{(d as any).path}</Card>
      ))}
    </div>
  );
};

export default Diffs;
