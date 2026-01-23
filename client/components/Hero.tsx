'use client';

import React, { useState } from 'react';
import { Search } from 'lucide-react';

interface HeroProps {
  onSearch: (query: string) => void;
}

const Hero: React.FC<HeroProps> = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) onSearch(query);
  };

  return (
    <div className="max-w-7xl mx-auto px-6 lg:px-8 pt-32 pb-24">
      <div className="max-w-3xl">
        <span className="text-[11px] font-bold uppercase tracking-[0.25em] text-slate-400 mb-6 block">
          Official Campus Navigator
        </span>
        
        <h1 className="text-5xl lg:text-7xl font-bold tracking-tight text-slate-900 leading-none mb-10">
          Intelligent routing for <br />
          <span className="text-emerald-600">ASTU Campus.</span>
        </h1>

        <p className="text-lg text-slate-500 leading-relaxed max-w-xl mb-12">
          Find any facility or department across the Adama Science and Technology University with our official navigation engine.
        </p>

        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-0 max-w-2xl mb-24 group">
          <div className="relative flex-grow">
            <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Where do you want to go?"
              className="w-full pl-16 pr-6 py-5 bg-white border border-slate-200 rounded-l-2xl focus:ring-0 focus:border-slate-300 outline-none text-slate-900 text-lg shadow-sm"
            />
          </div>
          <button 
            type="submit"
            className="px-10 py-5 bg-slate-800 text-white rounded-r-2xl font-bold hover:bg-slate-900 transition-all text-lg"
          >
            Find Route
          </button>
        </form>

        <div className="flex flex-wrap gap-x-16 gap-y-4 pt-12 border-t border-slate-100">
          <span className="text-xs font-bold uppercase tracking-widest text-slate-400">100% Campus Coverage</span>
          <span className="text-xs font-bold uppercase tracking-widest text-slate-400">Live AI Reasoning</span>
          <span className="text-xs font-bold uppercase tracking-widest text-slate-400">Secure Academic Data</span>
        </div>
      </div>
    </div>
  );
};

export default Hero;
