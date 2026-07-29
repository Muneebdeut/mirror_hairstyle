'use client';

import React from 'react';
import { StylePreferenceType } from '@/types';
import { Sparkles, Info } from 'lucide-react';

interface PreferenceSelectorProps {
  selectedPreference: StylePreferenceType;
  onChangePreference: (pref: StylePreferenceType) => void;
}

const PREFERENCE_OPTIONS: { id: StylePreferenceType; label: string; desc: string }[] = [
  {
    id: 'masculine',
    label: 'Masculine',
    desc: 'Prioritize masculine and unisex hairstyles'
  },
  {
    id: 'feminine',
    label: 'Feminine',
    desc: 'Prioritize feminine and unisex hairstyles'
  },
  {
    id: 'unisex',
    label: 'Unisex',
    desc: 'Prioritize versatile unisex hairstyles'
  },
  {
    id: 'no_preference',
    label: 'No Preference',
    desc: 'Consider all hairstyles based on face shape & hair fit'
  }
];

export const PreferenceSelector: React.FC<PreferenceSelectorProps> = ({
  selectedPreference,
  onChangePreference,
}) => {
  return (
    <div className="w-full max-w-4xl mx-auto rounded-3xl bg-slate-900/80 border border-white/10 p-6 sm:p-8 backdrop-blur-xl shadow-xl">
      <div className="flex items-center gap-3 mb-2">
        <div className="p-2 rounded-xl bg-brand-500/10 border border-brand-500/20 text-brand-400">
          <Sparkles className="w-5 h-5" />
        </div>
        <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
          What type of hairstyles would you like to explore?
        </h3>
      </div>
      <p className="text-slate-400 text-sm mb-6 ml-11">
        Select your style preference to customize recommendation ranking. You can change this selection at any time.
      </p>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        {PREFERENCE_OPTIONS.map((opt) => {
          const isSelected = selectedPreference === opt.id;
          return (
            <button
              key={opt.id}
              onClick={() => onChangePreference(opt.id)}
              className={`relative flex flex-col items-center text-center p-4 sm:p-5 rounded-2xl border transition-all duration-300 ${
                isSelected
                  ? 'border-brand-500 bg-brand-500/15 text-white shadow-lg shadow-brand-500/20 scale-[1.02]'
                  : 'border-white/10 bg-slate-950/40 text-slate-300 hover:border-white/20 hover:bg-slate-950/70'
              }`}
            >
              <span className={`text-base font-bold mb-1 ${isSelected ? 'text-brand-300' : 'text-white'}`}>
                {opt.label}
              </span>
              <span className="text-[11px] text-slate-400 leading-tight">
                {opt.desc}
              </span>
              {isSelected && (
                <div className="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-brand-400 shadow-md shadow-brand-400/50" />
              )}
            </button>
          );
        })}
      </div>

      <div className="mt-6 pt-4 border-t border-white/5 flex items-center gap-2 text-xs text-slate-400">
        <Info className="w-4 h-4 text-brand-400 shrink-0" />
        <span>Preference filter acts as a ranking factor. Styles across all categories remain discoverable.</span>
      </div>
    </div>
  );
};
