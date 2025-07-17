import React from 'react';
import ThemeToggle from './ThemeToggle';
import OllamaStatus from './OllamaStatus';

const Header: React.FC = () => (
  <header className="flex items-center justify-between p-4 bg-surface shadow-lg" role="banner">
    <h1 className="text-xl font-bold">AlgoriPS</h1>
    <div className="flex items-center gap-4">
      <OllamaStatus />
      <ThemeToggle />
    </div>
  </header>
);

export default Header;
