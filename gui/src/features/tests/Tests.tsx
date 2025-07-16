import React, { useEffect, useState } from 'react';
import { useAppStore } from '../../store';
import Card from '../../components/Card';
import Spinner from '../../components/Spinner';

const Tests: React.FC = () => {
  const report = useAppStore(state => state.testReport);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
  }, []);

  if (loading) return <Spinner />;
  return (
    <div>
      <h2>Tests</h2>
      <Card>{report ? JSON.stringify(report) : 'No report'}</Card>
    </div>
  );
};

export default Tests;

