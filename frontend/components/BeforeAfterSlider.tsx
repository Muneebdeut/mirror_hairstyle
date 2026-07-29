'use client';

import React, { useState, useRef, useCallback, useEffect } from 'react';
import { ChevronsLeftRight } from 'lucide-react';

interface BeforeAfterSliderProps {
  beforeImageUrl: string;
  afterImageUrl: string;
  beforeLabel?: string;
  afterLabel?: string;
}

export const BeforeAfterSlider: React.FC<BeforeAfterSliderProps> = ({
  beforeImageUrl,
  afterImageUrl,
  beforeLabel = 'BEFORE',
  afterLabel = 'AFTER',
}) => {
  const [sliderPosition, setSliderPosition] = useState(50);
  const [isDragging, setIsDragging] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMove = useCallback((clientX: number) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = clientX - rect.left;
    let positionPct = (x / rect.width) * 100;
    positionPct = Math.max(0, Math.min(100, positionPct));
    setSliderPosition(positionPct);
  }, []);

  const handleTouchMove = useCallback((e: TouchEvent) => {
    if (!isDragging) return;
    handleMove(e.touches[0].clientX);
  }, [isDragging, handleMove]);

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (!isDragging) return;
    handleMove(e.clientX);
  }, [isDragging, handleMove]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  useEffect(() => {
    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
      window.addEventListener('touchmove', handleTouchMove);
      window.addEventListener('touchend', handleMouseUp);
    }
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
      window.removeEventListener('touchmove', handleTouchMove);
      window.removeEventListener('touchend', handleMouseUp);
    };
  }, [isDragging, handleMouseMove, handleMouseUp, handleTouchMove]);

  return (
    <div
      ref={containerRef}
      onMouseDown={() => setIsDragging(true)}
      onTouchStart={() => setIsDragging(true)}
      className="relative aspect-[3/4] max-h-[560px] w-full max-w-lg mx-auto rounded-3xl overflow-hidden select-none cursor-ew-resize border border-white/10 shadow-2xl bg-slate-950"
    >
      {/* AFTER IMAGE (Full Layer) */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={afterImageUrl}
        alt="AI Virtual Try-On Result"
        className="absolute inset-0 w-full h-full object-cover"
      />
      <div className="absolute top-4 right-4 px-3 py-1 rounded-full bg-brand-500/80 backdrop-blur-md text-white text-xs font-black tracking-wider uppercase shadow-md">
        {afterLabel}
      </div>

      {/* BEFORE IMAGE (Clipped Layer) */}
      <div
        className="absolute inset-0 overflow-hidden"
        style={{ width: `${sliderPosition}%` }}
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={beforeImageUrl}
          alt="Original User Portrait"
          className="absolute top-0 left-0 h-full max-w-none object-cover"
          style={{ width: containerRef.current ? `${containerRef.current.clientWidth}px` : '100%' }}
        />
        <div className="absolute top-4 left-4 px-3 py-1 rounded-full bg-slate-900/80 backdrop-blur-md text-white text-xs font-black tracking-wider uppercase shadow-md">
          {beforeLabel}
        </div>
      </div>

      {/* DRAGGABLE SLIDER DIVIDER BAR */}
      <div
        className="absolute top-0 bottom-0 w-1 bg-white shadow-[0_0_10px_rgba(255,255,255,0.8)] cursor-ew-resize flex items-center justify-center"
        style={{ left: `${sliderPosition}%` }}
      >
        <div className="w-10 h-10 -ml-4 rounded-full bg-white text-slate-900 shadow-xl flex items-center justify-center border-2 border-brand-500 hover:scale-110 active:scale-95 transition-transform">
          <ChevronsLeftRight className="w-5 h-5 text-brand-600" />
        </div>
      </div>
    </div>
  );
};
