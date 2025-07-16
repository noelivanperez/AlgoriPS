import create from 'zustand';

export interface AnalysisResult {}
export interface DiffFile {}
export interface TestReport {}
export interface Settings {}

interface AppState {
  projectPath: string;
  analysisResult?: AnalysisResult;
  diffs: DiffFile[];
  testReport?: TestReport;
  settings?: Settings;

  setProjectPath: (path: string) => void;
  setAnalysisResult: (res: AnalysisResult) => void;
  setDiffs: (d: DiffFile[]) => void;
  setTestReport: (r: TestReport) => void;
  setSettings: (s: Settings) => void;
}

export const useAppStore = create<AppState>((set) => ({
  projectPath: '',
  diffs: [],
  setProjectPath: (projectPath) => set({ projectPath }),
  setAnalysisResult: (analysisResult) => set({ analysisResult }),
  setDiffs: (diffs) => set({ diffs }),
  setTestReport: (testReport) => set({ testReport }),
  setSettings: (settings) => set({ settings }),
}));
