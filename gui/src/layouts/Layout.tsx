import React from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

const Layout: React.FC<React.PropsWithChildren> = ({ children }) => (
  <div className="app-layout">
    <Sidebar />
    <div className="app-main">
      <Header />
      {children}
    </div>
  </div>
);

export default Layout;
