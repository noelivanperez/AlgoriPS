import React from 'react';
import "./src/styles/theme.css";
import { createRoot } from 'react-dom/client';
import Layout from './src/layouts/Layout';
import Home from './src/features/home/Home';
import Analyze from './src/features/analyze/Analyze';
import Repository from './src/features/repository/Repository';
import Plugins from './src/features/plugins/Plugins';
import Metrics from './src/features/metrics/Metrics';
import { useAppStore } from './src/store';

const RootApp: React.FC = () => {
  const projectPath = useAppStore(state => state.projectPath);
  return (
    <Layout>
      {projectPath ? <Analyze /> : <Home />}
      <Repository />
      <Plugins />
      <Metrics />
    </Layout>
  );
};

const root = createRoot(document.getElementById('root')!);
root.render(<RootApp />);
