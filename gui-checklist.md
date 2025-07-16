# Checklist de Fase 2 – GUI

- [x] Inicializar proyecto GUI con Electron, React y TypeScript  
- [x] Instalar dependencias: React, TypeScript, shadcn/ui, lucide-react, recharts, Zustand  
- [x] Crear estructura de carpetas `/gui` según convención:
  ```
  /gui
  ├─ /public
  ├─ /src
  │   ├─ /components
  │   ├─ /layouts
  │   ├─ /features/analyze
  │   ├─ /features/diffs
  │   ├─ /features/tests
  │   ├─ /features/settings
  │   └─ /features/home
  ├─ electron.ts
  ├─ index.tsx
  ├─ package.json
  └─ tsconfig.json
  ```
- [x] Diseñar wireframes para vistas Home, Analyze, Diffs, Tests y Settings (colocar en `docs/gui_wireframes/`)  
- [x] Implementar layout global: Sidebar, Header, Card, Modal y Spinner con shadcn/ui  
- [x] Configurar estado global (Zustand o Redux Toolkit) con:
  - `projectPath`
  - `analysisResult`
  - `diffs`
  - `testReport`
  - `settings`
- [x] Implementar utilidades de API en `src/utils/api.ts`:
  - `analyze(path): Promise<AnalysisResult>`
  - `getDiffs(): Promise<DiffFile[]>`
  - `runTests(suite?): Promise<TestReport>`
  - `saveSettings(cfg): Promise<void>`
- [x] Construir pantalla **Home** con selector de carpeta y navegación  
- [x] Construir pantalla **Analyze** con tarjetas de métricas y gráfica con recharts  
- [x] Construir pantalla **Diffs**: lista de archivos, editor Monaco y acciones de patch  
- [x] Construir pantalla **Tests** con lista de suites, progreso y visor de resultados  
- [x] Construir pantalla **Settings** con formulario validado y persistencia en `algorips.yaml`  
- [x] Escribir tests de UI con Jest + React Testing Library para cada componente y flujo  
- [x] Configurar scripts de empaquetado (`npm run make`) con Electron Builder para Windows y macOS  
- [x] Documentar instalación y uso en `docs/gui_setup.md`  
- [x] Validación general: ejecutar todas las pruebas unitarias, corregir cualquier error y optimizar donde sea necesario  
