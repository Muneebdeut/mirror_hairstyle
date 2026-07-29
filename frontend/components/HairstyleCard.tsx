'use client';

import React from 'react';
import { Sparkles, ArrowRight, Clock, Award } from 'lucide-react';
import { RecommendationItem } from '@/types';

interface HairstyleCardProps {
  item: RecommendationItem;
  onSelect: (item: RecommendationItem) => void;
  isSelected?: boolean;
}

export const HairstyleCard: React.FC<HairstyleCardProps> = ({
  item,
  onSelect,
  isSelected = false,
}) => {
  const { hairstyle, name, match_score, reason } = item;

  return (
    <div
      className={`relative flex flex-col justify-between rounded-3xl border transition-all duration-300 p-6 backdrop-blur-xl bg-slate-900/80 hover:bg-slate-900 shadow-xl ${
        isSelected
          ? 'border-brand-500 ring-2 ring-brand-500/50 scale-[1.02]'
          : 'border-white/10 hover:border-brand-400/50'
      }`}
    >
      <div className="space-y-4">
        {/* Top Badges */}
        <div className="flex items-center justify-between gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold font-mono">
            <Award className="w-3.5 h-3.5" />
            {match_score}% Match
          </span>

          <span className="text-xs font-medium text-slate-400 capitalize px-2.5 py-0.5 rounded-md bg-white/5 border border-white/5">
            {hairstyle.presentation}
          </span>
        </div>

        {/* Title */}
        <div>
          <h4 className="text-xl font-black text-white tracking-tight uppercase">
            {name}
          </h4>
          <div className="flex items-center gap-3 text-xs text-slate-400 mt-1">
            <span>{hairstyle.category}</span>
            <span>•</span>
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3 text-brand-400" />
              {hairstyle.maintenance} Maintenance
            </span>
          </div>
        </div>

        {/* Description */}
        <p className="text-slate-300 text-sm line-clamp-2 leading-relaxed">
          {hairstyle.description}
        </p>

        {/* Recommendation Reason */}
        <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-white/5 space-y-1">
          <span className="text-[11px] font-bold text-brand-300 uppercase tracking-wider block">
            Why we recommend it:
          </span>
          <p className="text-xs text-slate-300 leading-normal">
            {reason}
          </p>
        </div>
      </div>

      {/* Action CTA Button */}
      <div className="mt-6 pt-4 border-t border-white/5">
        <button
          onClick={() => onSelect(item)}
          className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white font-bold text-sm shadow-lg shadow-brand-500/25 hover:shadow-brand-500/40 transition-all hover:scale-[1.02] active:scale-95"
        >
          <Sparkles className="w-4 h-4" />
          Try This Hairstyle
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
