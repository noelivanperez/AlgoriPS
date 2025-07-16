import React from 'react';
import { useAppStore } from '../../store';
import Card from '../../components/Card';
import { LineChart, Line, XAxis, YAxis } from 'recharts';

const Analyze: React.FC = () => {
  const result = useAppStore(state => state.analysisResult);
  const data = result ? (result as any).metrics || [] : [];

  return (
    <div>
      <h2>Analysis</h2>
      <Card>
        <LineChart width={400} height={200} data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Line type="monotone" dataKey="value" stroke="#8884d8" />
        </LineChart>
      </Card>
    </div>
  );
};

export default Analyze;
