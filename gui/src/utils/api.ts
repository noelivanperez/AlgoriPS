import { AnalysisResult, DiffFile, TestReport, Settings } from '../store';

export async function analyze(path: string): Promise<AnalysisResult> {
  console.log('analyze', path);
  return {} as AnalysisResult;
}

export async function getDiffs(): Promise<DiffFile[]> {
  console.log('getDiffs');
  return [];
}

export async function runTests(suite?: string): Promise<TestReport> {
  console.log('runTests', suite);
  return {} as TestReport;
}

export async function saveSettings(cfg: Settings): Promise<void> {
  console.log('saveSettings', cfg);
}

// Repository API stubs
export async function cloneRepo(url: string, dest: string): Promise<void> {
  console.log('cloneRepo', url, dest);
}

export async function createBranch(name: string): Promise<void> {
  console.log('createBranch', name);
}

export async function commitChanges(msg: string): Promise<void> {
  console.log('commitChanges', msg);
}

export async function listPullRequests(): Promise<any[]> {
  console.log('listPullRequests');
  return [];
}

export async function openPullRequest(): Promise<void> {
  console.log('openPullRequest');
}

export async function mergePullRequest(num: number): Promise<void> {
  console.log('mergePullRequest', num);
}

// Plugin API stubs
export async function listPlugins(): Promise<any[]> {
  console.log('listPlugins');
  return [];
}

export async function installPlugin(path: string): Promise<void> {
  console.log('installPlugin', path);
}

export async function uninstallPlugin(name: string): Promise<void> {
  console.log('uninstallPlugin', name);
}

// Database API
export async function executeQuery(
  name: string,
  sql: string,
  params?: Record<string, unknown>
): Promise<any[]> {
  const resp = await fetch('/db/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, sql, params }),
  });
  return resp.json();
}

export async function chatWithOllama(prompt: string, db: string): Promise<ReadableStreamDefaultReader<Uint8Array>> {
  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, db }),
  });
  const reader = res.body?.getReader();
  if (!reader) {
    throw new Error('Streaming not supported');
  }
  return reader;
}

export async function isOllamaUp(): Promise<boolean> {
  try {
    const url = (process as any).env.OLLAMA_URL || 'http://localhost:11434';
    const res = await fetch(url, { method: 'HEAD' });
    return res.ok;
  } catch {
    return false;
  }
}
