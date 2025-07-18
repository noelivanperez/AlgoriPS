export interface MetricPoint {
  name: string;
  value: number;
}

export default function parseMetrics(text: string): MetricPoint[] {
  const counters: MetricPoint[] = [];
  const lines = text.split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const parts = trimmed.split(/\s+/);
    if (parts.length !== 2) {
      throw new Error(`Invalid metric line: ${line}`);
    }
    const [key, val] = parts;
    const num = parseFloat(val);
    if (isNaN(num)) {
      throw new Error(`Invalid metric value: ${line}`);
    }
    if (key.endsWith('_total')) {
      counters.push({ name: key, value: num });
    }
  }
  return counters;
}
