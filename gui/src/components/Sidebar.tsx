import React from 'react';
import { Layers, Wand2, FlaskConical, Plug } from 'lucide-react';

const Sidebar: React.FC = () => (
  <nav className="sidebar">
    <ul>
      <li><Layers size={20}/> Análisis</li>
      <li><Wand2 size={20}/> Refactor</li>
      <li><FlaskConical size={20}/> Tests</li>
      <li><Plug size={20}/> Plugins</li>
    </ul>
  </nav>
);

export default Sidebar;
