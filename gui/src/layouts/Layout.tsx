import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import Footer from '../components/Footer';

const Layout: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="min-h-screen md:grid md:grid-cols-[auto_1fr]">
      <Sidebar active="Dashboard" />
      <button
        className="md:hidden p-2 m-2 rounded bg-primary text-white"
        onClick={() => setOpen(!open)}
        aria-label="toggle-menu"
      >
        ☰
      </button>
      {open && (
        <div className="md:hidden">
          <Sidebar />
        </div>
      )}
      <main className="flex flex-col">
        <Header />
        <div className="flex-1 container mx-auto p-4 md:p-8 space-y-12">
          {children}
        </div>
        <Footer />
      </main>
    </div>
  );
};

export default Layout;

