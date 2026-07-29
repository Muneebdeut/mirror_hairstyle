'use client';

import React from 'react';
import { BeforeAfterSlider } from './BeforeAfterSlider';
import { Download, RefreshCw, Sparkles, ArrowLeft } from 'lucide-react';
import { RecommendationItem } from '@/types';

interface TryOnResultProps {
  originalImageUrl: string;
  tryOnImageUrl: string;
  selectedHairstyle: RecommendationItem;
  onTryAnother: () => void;
  onStartOver: () => void;
}

export const TryOnResult: React.FC<TryOnResultProps> = ({
  originalImageUrl,
  tryOnImageUrl,
  selectedHairstyle,
  onTryAnother,
  onStartOver,
}) => {
  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = tryOnImageUrl;
    link.download = `ai-hairstyle-${selectedHairstyle.hairstyle.id}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs font-semibold uppercase tracking-wider">
          <Sparkles className="w-4 h-4" />
          AI Virtual Hairstyle Preview
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Your New Look: <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-300 to-gold-400 uppercase">{selectedHairstyle.name}</span>
        </h2>
        <p className="text-slate-400 text-sm max-w-md mx-auto">
          Drag the center slider horizontally to compare your original photo with the AI virtual try-on preview.
        </p>
      </div>

      {/* Before / After Interactive Visual Slider */}
      <BeforeAfterSlider
        beforeImageUrl={originalImageUrl}
        afterImageUrl={tryOnImageUrl}
        beforeLabel="Original Photo"
        afterLabel={`${selectedHairstyle.name} Preview`}
      />

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-lg mx-auto pt-4">
        <button
          onClick={onTryAnother}
          className="w-full sm:w-auto flex-1 flex items-center justify-center gap-2 py-3.5 px-6 rounded-2xl bg-slate-900 border border-white/10 hover:border-brand-400/50 text-white font-bold text-sm shadow-xl transition-all hover:scale-105 active:scale-95"
        >
          <ArrowLeft className="w-4 h-4" />
          Try Another Hairstyle
        </button>

        <button
          onClick={handleDownload}
          className="w-full sm:w-auto flex-1 flex items-center justify-center gap-2 py-3.5 px-6 rounded-2xl bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white font-bold text-sm shadow-xl shadow-brand-500/25 transition-all hover:scale-105 active:scale-95"
        >
          <Download className="w-4 h-4" />
          Download Result
        </button>

        <button
          onClick={onStartOver}
          className="w-full sm:w-auto flex flex-items-center justify-center gap-2 py-3.5 px-6 rounded-2xl bg-slate-950/60 border border-white/5 hover:bg-slate-900 text-slate-400 hover:text-white font-medium text-sm transition-all"
        >
          <RefreshCw className="w-4 h-4" />
          Start Over
        </button>
      </div>
    </div>
  );
};
