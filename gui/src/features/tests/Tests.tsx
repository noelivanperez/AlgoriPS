import React from 'react';
import { useAppStore } from '../../store';
import Card from '../../components/Card';

const Tests: React.FC = () => {
  const report = useAppStore(state => state.testReport);
  return (
    <div>
      <h2>Tests</h2>
      <Card>{report ? JSON.stringify(report) : 'No report'}</Card>
    </div>
  );
};

export default Tests;
