import React from 'react';
import { Layers, Wand2, MessageCircle, FlaskConical, Database } from 'lucide-react';

const items = [
  { icon: Layers, label: 'Análisis' },
  { icon: Wand2, label: 'Refactor' },
  { icon: MessageCircle, label: 'Chat' },
  { icon: FlaskConical, label: 'Scraping' },
  { icon: Database, label: 'BD' },
];

interface SidebarProps {
  active?: string;
}

const Sidebar: React.FC<SidebarProps> = ({ active }) => (
  <nav
    className="h-full bg-surface border-r border-gray-200 p-4 hidden md:block md:w-60 lg:w-72"
    aria-label="Sidebar"
  >
    <ul className="space-y-4">
      {items.map(({ icon: Icon, label }) => (
        <li key={label} className={label === active ? 'text-primary font-semibold' : ''}>
          <a href="#" className="flex items-center gap-2">
            <Icon className="w-5 h-5" />
            {label}
          </a>
        </li>
      ))}
    </ul>
  </nav>
);

export default Sidebar;
