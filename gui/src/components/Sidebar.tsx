import React from 'react';
import { Home, Search, GitBranch, Play, Settings, GitPullRequest } from 'lucide-react';

const Sidebar: React.FC = () => (
  <nav className="sidebar">
    <ul>
      <li><Home size={20}/> Home</li>
      <li><Search size={20}/> Analyze</li>
      <li><GitBranch size={20}/> Diffs</li>
      <li><GitPullRequest size={20}/> Repository</li>
      <li><Play size={20}/> Tests</li>
      <li><Settings size={20}/> Settings</li>
    </ul>
  </nav>
);

export default Sidebar;
