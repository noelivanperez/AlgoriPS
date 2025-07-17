import React from 'react';
import ThemeToggle from './ThemeToggle';

const Header: React.FC = () => (
  <header className="flex items-center justify-between p-4 bg-surface shadow-lg" role="banner">
    <h1 className="text-xl font-bold">AlgoriPS</h1>
    <ThemeToggle />
  </header>
);

export default Header;
