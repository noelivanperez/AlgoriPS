import React from 'react';
import { BarChart2, ClipboardList, Timer } from 'lucide-react';

const metrics = [
  { icon: <ClipboardList className="w-6 h-6" />, label: 'Análisis', value: 24 },
  { icon: <BarChart2 className="w-6 h-6" />, label: 'Cobertura', value: '85%' },
  { icon: <Timer className="w-6 h-6" />, label: 'Latencia', value: '120ms' },
];

const Dashboard: React.FC = () => (
  <div className="p-4 grid gap-6 sm:grid-cols-2 md:grid-cols-3">
    {metrics.map((m, idx) => (
      <div key={idx} className="rounded-2xl shadow-lg bg-surface p-4 flex items-center space-x-4">
        {m.icon}
        <div>
          <div className="text-2xl font-bold" aria-label="metric-value">{m.value}</div>
          <div className="text-sm text-gray-500" aria-label="metric-label">{m.label}</div>
        </div>
      </div>
    ))}
  </div>
);

export default Dashboard;
