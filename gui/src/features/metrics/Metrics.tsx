import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

interface MetricPoint {
  name: string;
  value: number;
}

const Metrics: React.FC = () => {
  const [data, setData] = useState<MetricPoint[]>([]);

  const fetchMetrics = async () => {
    try {
      const res = await fetch('/metrics');
      const text = await res.text();
      const counters: MetricPoint[] = [];
      text.split('\n').forEach(line => {
        if (line.startsWith('#')) return;
        const [key, val] = line.split(' ');
        if (key && val && key.endsWith('_total')) {
          counters.push({ name: key, value: parseFloat(val) });
        }
      });
      setData(counters);
    } catch (err) {
      console.error('Failed to load metrics', err);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const id = setInterval(fetchMetrics, 5000);
    return () => clearInterval(id);
  }, []);

  return (
    <div>
      <h2>Metrics</h2>
      <LineChart width={400} height={200} data={data} aria-label="Metrics chart">
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis allowDecimals={false} />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
      </LineChart>
    </div>
  );
};

export default Metrics;
