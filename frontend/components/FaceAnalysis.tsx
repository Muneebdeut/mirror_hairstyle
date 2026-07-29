'use client';

import React, { useState } from 'react';
import { Sparkles, Edit3, ShieldAlert, Check, SlidersHorizontal } from 'lucide-react';
import { FaceAnalysisResult, HairCharacteristics } from '@/types';

interface FaceAnalysisProps {
  analysis: FaceAnalysisResult;
  hairCharacteristics: HairCharacteristics;
  onUpdateHairCharacteristics: (updated: HairCharacteristics) => void;
  onUpdateFaceShape?: (newShape: string) => void;
}

export const FaceAnalysis: React.FC<FaceAnalysisProps> = ({
  analysis,
  hairCharacteristics,
  onUpdateHairCharacteristics,
  onUpdateFaceShape,
}) => {
  const [isEditingHair, setIsEditingHair] = useState(false);
  const [editedHair, setEditedHair] = useState<HairCharacteristics>(hairCharacteristics);
  const [isEditingShape, setIsEditingShape] = useState(false);
  const [selectedShape, setSelectedShape] = useState<string>(analysis.face_shape || 'Oval');

  const confidencePct = Math.round((analysis.confidence || 0.85) * 100);

  const handleSaveHair = () => {
    onUpdateHairCharacteristics(editedHair);
    setIsEditingHair(false);
  };

  const handleSaveShape = (shape: string) => {
    setSelectedShape(shape);
    setIsEditingShape(false);
    if (onUpdateFaceShape) {
      onUpdateFaceShape(shape);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      {/* Face Shape Primary Card */}
      <div className="relative overflow-hidden rounded-3xl bg-slate-900/80 border border-white/10 p-6 sm:p-8 backdrop-blur-xl shadow-2xl">
        <div className="absolute top-0 right-0 w-64 h-64 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs font-semibold uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5" />
              Facial Landmark Analysis
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Your Estimated Face Shape
            </h2>
            <p className="text-slate-400 text-sm">
              Detected based on forehead, cheekbone, and jaw geometric ratios.
            </p>
          </div>

          <div className="flex flex-col items-start sm:items-end bg-slate-950/60 border border-white/10 p-4 sm:p-5 rounded-2xl min-w-[220px]">
            {isEditingShape ? (
              <div className="space-y-2 w-full">
                <label className="text-[11px] font-bold text-slate-400 uppercase block">Select Shape</label>
                <select
                  value={selectedShape}
                  onChange={(e) => handleSaveShape(e.target.value)}
                  className="w-full bg-slate-900 border border-brand-500 rounded-xl px-2 py-1.5 text-sm font-bold text-brand-300 focus:outline-none"
                >
                  <option value="Oval">Oval</option>
                  <option value="Round">Round</option>
                  <option value="Square">Square</option>
                  <option value="Heart">Heart</option>
                  <option value="Oblong">Oblong</option>
                </select>
              </div>
            ) : (
              <>
                <div className="flex items-center gap-2">
                  <span className="text-3xl sm:text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-brand-300 via-white to-gold-400 uppercase tracking-wide">
                    {selectedShape}
                  </span>
                  <button
                    onClick={() => setIsEditingShape(true)}
                    className="p-1 rounded-md hover:bg-white/10 text-slate-400 hover:text-brand-300 transition-colors"
                    title="Change Face Shape"
                  >
                    <Edit3 className="w-4 h-4" />
                  </button>
                </div>
                <span className="text-xs font-semibold text-brand-400 mt-1">
                  {confidencePct}% Confidence
                </span>
              </>
            )}
          </div>
        </div>

        {/* Geometric Measurements Bar Matrix */}
        {analysis.measurements && (
          <div className="mt-8 pt-6 border-t border-white/5 grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-slate-950/40 p-3.5 rounded-xl border border-white/5">
              <span className="text-xs text-slate-400 block">Face Length</span>
              <span className="text-lg font-bold text-white font-mono">{analysis.measurements.face_length} px</span>
            </div>
            <div className="bg-slate-950/40 p-3.5 rounded-xl border border-white/5">
              <span className="text-xs text-slate-400 block">Cheekbone Width</span>
              <span className="text-lg font-bold text-white font-mono">{analysis.measurements.cheekbone_width} px</span>
            </div>
            <div className="bg-slate-950/40 p-3.5 rounded-xl border border-white/5">
              <span className="text-xs text-slate-400 block">Jaw Width</span>
              <span className="text-lg font-bold text-white font-mono">{analysis.measurements.jaw_width} px</span>
            </div>
            <div className="bg-slate-950/40 p-3.5 rounded-xl border border-white/5">
              <span className="text-xs text-slate-400 block">Aspect Ratio</span>
              <span className="text-lg font-bold text-brand-300 font-mono">{analysis.measurements.aspect_ratio}</span>
            </div>
          </div>
        )}

        <div className="mt-6 flex items-start gap-2.5 text-xs text-slate-400 bg-slate-950/30 p-3 rounded-xl border border-white/5">
          <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <span>{analysis.disclaimer || 'Face shape is an AI-based estimate and may not be perfectly accurate.'}</span>
        </div>
      </div>

      {/* Hair Analysis Summary & Edit Card */}
      <div className="rounded-3xl bg-slate-900/60 border border-white/10 p-6 backdrop-blur-xl shadow-xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-brand-500/10 border border-brand-500/20 text-brand-400">
              <SlidersHorizontal className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">AI Hair Analysis</h3>
              <p className="text-xs text-slate-400">Detected characteristics of your hair</p>
            </div>
          </div>

          <button
            onClick={() => setIsEditingHair(!isEditingHair)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-xs font-medium text-brand-300 border border-white/10 transition-all"
          >
            <Edit3 className="w-3.5 h-3.5" />
            {isEditingHair ? 'Cancel' : 'Edit Hair Profile'}
          </button>
        </div>

        {isEditingHair ? (
          <div className="space-y-4 pt-2">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="text-xs text-slate-300 mb-1.5 block font-medium">Hair Length</label>
                <select
                  value={editedHair.hair_length}
                  onChange={(e) => setEditedHair({ ...editedHair, hair_length: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-brand-500"
                >
                  <option value="Very Short">Very Short</option>
                  <option value="Short">Short</option>
                  <option value="Medium">Medium</option>
                  <option value="Long">Long</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-slate-300 mb-1.5 block font-medium">Hair Texture</label>
                <select
                  value={editedHair.hair_texture}
                  onChange={(e) => setEditedHair({ ...editedHair, hair_texture: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-brand-500"
                >
                  <option value="Straight">Straight</option>
                  <option value="Wavy">Wavy</option>
                  <option value="Curly">Curly</option>
                  <option value="Coily">Coily</option>
                  <option value="Unknown">Unknown</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-slate-300 mb-1.5 block font-medium">Hair Density</label>
                <select
                  value={editedHair.hair_density}
                  onChange={(e) => setEditedHair({ ...editedHair, hair_density: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-brand-500"
                >
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                  <option value="Unknown">Unknown</option>
                </select>
              </div>
            </div>

            <button
              onClick={handleSaveHair}
              className="flex items-center gap-2 px-5 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold transition-all shadow-md"
            >
              <Check className="w-4 h-4" />
              Save Hair Profile
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-3 gap-4 pt-2">
            <div className="bg-slate-950/50 p-3 rounded-2xl border border-white/5">
              <span className="text-xs text-slate-400 block">Length</span>
              <span className="text-sm font-semibold text-white">{hairCharacteristics.hair_length}</span>
            </div>
            <div className="bg-slate-950/50 p-3 rounded-2xl border border-white/5">
              <span className="text-xs text-slate-400 block">Texture</span>
              <span className="text-sm font-semibold text-white">{hairCharacteristics.hair_texture}</span>
            </div>
            <div className="bg-slate-950/50 p-3 rounded-2xl border border-white/5">
              <span className="text-xs text-slate-400 block">Density</span>
              <span className="text-sm font-semibold text-white">{hairCharacteristics.hair_density}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
