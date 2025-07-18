import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';
import parseMetrics, { MetricPoint } from '../../utils/metricsParser';

const Metrics: React.FC = () => {
  const [data, setData] = useState<MetricPoint[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchMetrics = async () => {
    try {
      const res = await fetch('/metrics');
      const text = await res.text();
      const counters = parseMetrics(text);
      setData(counters);
      setError(null);
    } catch (err) {
      console.error('Failed to load metrics', err);
      setError('Could not parse metrics');
    }
  };

  useEffect(() => {
    fetchMetrics();
    const id = setInterval(fetchMetrics, 5000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="space-y-4 max-w-5xl mx-auto">
      <h2 className="text-lg font-semibold">Metrics</h2>
      {error && (
        <div role="alert" style={{ color: 'red' }}>
          {error}
        </div>
      )}
      <div className="w-full h-60">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} aria-label="Metrics chart">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Metrics;
