import React from 'react';
import { Home, Search, GitBranch, Play, Settings } from 'lucide-react';

const Sidebar: React.FC = () => (
  <nav className="sidebar" aria-label="Main navigation">
    <ul>
      <li><a href="#home"><Home size={20} aria-hidden /> Home</a></li>
      <li><a href="#analyze"><Search size={20} aria-hidden /> Analyze</a></li>
      <li><a href="#diffs"><GitBranch size={20} aria-hidden /> Diffs</a></li>
      <li><a href="#tests"><Play size={20} aria-hidden /> Tests</a></li>
      <li><a href="#settings"><Settings size={20} aria-hidden /> Settings</a></li>
    </ul>
  </nav>
);


