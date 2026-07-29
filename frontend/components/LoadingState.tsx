'use client';

import React from 'react';
import { Loader2, Sparkles } from 'lucide-react';

interface LoadingStateProps {
  title?: string;
  subtitle?: string;
  step?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  title = 'AI Processing In Progress...',
  subtitle = 'Detecting facial landmarks, estimating face shape, and ranking hairstyles.',
  step = 'Analyzing photo geometry',
}) => {
  return (
    <div className="w-full max-w-lg mx-auto p-8 rounded-3xl bg-slate-900/80 border border-white/10 backdrop-blur-xl shadow-2xl text-center space-y-6 animate-pulse">
      <div className="relative w-20 h-20 mx-auto flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border-4 border-brand-500/20 border-t-brand-500 animate-spin" />
        <div className="p-4 rounded-full bg-brand-500/10 text-brand-400">
          <Sparkles className="w-8 h-8 animate-bounce" />
        </div>
      </div>

      <div className="space-y-2">
        <h3 className="text-xl font-bold text-white tracking-tight">{title}</h3>
        <p className="text-sm text-slate-400 leading-relaxed max-w-sm mx-auto">
          {subtitle}
        </p>
      </div>

      <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-950/60 border border-white/5 text-xs text-brand-300 font-mono">
        <Loader2 className="w-3.5 h-3.5 animate-spin" />
        <span>{step}</span>
      </div>
    </div>
  );
};
