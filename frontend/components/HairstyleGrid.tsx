'use client';

import React from 'react';
import { RecommendationItem } from '@/types';
import { HairstyleCard } from './HairstyleCard';
import { Sparkles } from 'lucide-react';

interface HairstyleGridProps {
  recommendations: RecommendationItem[];
  onSelectHairstyle: (item: RecommendationItem) => void;
  selectedHairstyle?: RecommendationItem | null;
}

export const HairstyleGrid: React.FC<HairstyleGridProps> = ({
  recommendations,
  onSelectHairstyle,
  selectedHairstyle,
}) => {
  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs font-semibold uppercase tracking-wider mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            Top Recommendations
          </div>
          <h3 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Recommended Hairstyles For You
          </h3>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {recommendations.map((item, idx) => (
          <HairstyleCard
            key={item.hairstyle.id || idx}
            item={item}
            onSelect={onSelectHairstyle}
            isSelected={selectedHairstyle?.hairstyle.id === item.hairstyle.id}
          />
        ))}
      </div>
    </div>
  );
};
