import React, { useEffect, useState } from 'react';
import { useAppStore } from '../../store';
import Card from '../../components/Card';
import Spinner from '../../components/Spinner';

const Diffs: React.FC = () => {
  const diffs = useAppStore(state => state.diffs);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
  }, []);

  if (loading) return <Spinner />;
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

