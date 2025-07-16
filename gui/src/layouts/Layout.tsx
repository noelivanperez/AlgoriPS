import React from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

const Layout: React.FC<React.PropsWithChildren> = ({ children }) => (
  <div className="app-layout">
    <Sidebar />
    <main className="app-main">
      <Header />
      {children}
    </main>
  </div>
);

export default Layout;

