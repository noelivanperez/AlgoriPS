import React from 'react';
import "./src/styles/theme.css";
import { createRoot } from 'react-dom/client';
import Layout from './src/layouts/Layout';
import Home from './src/features/home/Home';
import Analyze from './src/features/analyze/Analyze';
import Repository from './src/features/repository/Repository';
import Plugins from './src/features/plugins/Plugins';
import Chat from './src/features/chat/Chat';
import Metrics from './src/features/metrics/Metrics';
import Chat from './src/features/chat/Chat';
import { useAppStore } from './src/store';

const RootApp: React.FC = () => {
  const projectPath = useAppStore(state => state.projectPath);
  return (
    <Layout>
      {projectPath ? <Analyze /> : <Home />}
      <Repository />
      <Plugins />
      <Metrics />
      <Chat />
      <Chat />
    </Layout>
  );
};

const root = createRoot(document.getElementById('root')!);
root.render(<RootApp />);
