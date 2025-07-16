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
