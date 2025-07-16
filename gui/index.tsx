import React from 'react';
import { createRoot } from 'react-dom/client';
import Layout from './src/layouts/Layout';
import Home from './src/features/home/Home';
import Analyze from './src/features/analyze/Analyze';
import { useAppStore } from './src/store';

const RootApp: React.FC = () => {
  const projectPath = useAppStore(state => state.projectPath);
  return (
    <Layout>
      {projectPath ? <Analyze /> : <Home />}
    </Layout>
  );
};

const root = createRoot(document.getElementById('root')!);
root.render(<RootApp />);
