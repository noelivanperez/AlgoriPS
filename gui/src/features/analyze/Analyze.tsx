import React, { useEffect, useState } from 'react';
import { useAppStore } from '../../store';
import Card from '../../components/Card';
import Spinner from '../../components/Spinner';
import { LineChart, Line, XAxis, YAxis } from 'recharts';

const Analyze: React.FC = () => {
  const result = useAppStore(state => state.analysisResult);
  const [loading, setLoading] = useState(true);
  const data = result ? (result as any).metrics || [] : [];

  useEffect(() => {
    setLoading(false);
  }, []);

  if (loading) return <Spinner />;
  return (
    <div>
      <h2>Analysis</h2>
      <Card>
        <LineChart width={400} height={200} data={data} aria-label="Metrics chart">
          <XAxis dataKey="name" />
          <YAxis />
          <Line type="monotone" dataKey="value" stroke="#8884d8" />
        </LineChart>
      </Card>
    </div>
  );
};

export default Analyze;

