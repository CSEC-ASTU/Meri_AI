'use client';

import React from 'react';
import { AppRoute } from '../types';

interface NavbarProps {
  onNavigate: (route: AppRoute) => void;
  currentRoute: string;
}

const Navbar: React.FC<NavbarProps> = ({ onNavigate, currentRoute }) => {
  return (
    <nav className="bg-white border-b border-slate-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex justify-between h-20 items-center">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => onNavigate(AppRoute.HOME)}>
            <div className="w-8 h-8 bg-emerald-600 rounded flex items-center justify-center">
              <div className="w-4 h-4 border-2 border-white rounded-sm"></div>
            </div>
            <span className="font-bold text-slate-900 text-lg tracking-tight">ASTU Route AI</span>
          </div>
          
          <div className="hidden md:flex gap-10">
            <NavItem label="Home" active={currentRoute === AppRoute.HOME} onClick={() => onNavigate(AppRoute.HOME)} />
            <NavItem label="Campus Map" active={currentRoute === AppRoute.MAP} onClick={() => onNavigate(AppRoute.MAP)} />
            <NavItem label="Directory" active={currentRoute === AppRoute.DIRECTORY} onClick={() => onNavigate(AppRoute.DIRECTORY)} />
            <NavItem label="Assistant" active={currentRoute === AppRoute.ASSISTANT} onClick={() => onNavigate(AppRoute.ASSISTANT)} />
          </div>

          <div className="flex items-center">
            <button 
              onClick={() => onNavigate(AppRoute.MAP)}
              className="text-sm font-bold px-6 py-2.5 bg-slate-50 text-slate-900 border border-slate-200 rounded-lg hover:bg-slate-100 transition-colors active:scale-95"
            >
              Launch System
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

const NavItem: React.FC<{ label: string, active: boolean, onClick: () => void }> = ({ label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`text-sm font-semibold tracking-wide transition-colors ${
      active ? 'text-emerald-600' : 'text-slate-500 hover:text-slate-900'
    }`}
  >
    {label}
  </button>
);

export default Navbar;
