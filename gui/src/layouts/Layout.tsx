import React from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import Footer from '../components/Footer';

const Layout: React.FC<React.PropsWithChildren> = ({ children }) => (
  <div className="app-layout">
    <Sidebar />
    <main className="app-main">
      <Header />
      {children}
      <Footer />
    </main>
  </div>
);

export default Layout;

