'use client';

import React, { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { Upload, Camera, Image as ImageIcon, AlertCircle, RefreshCw } from 'lucide-react';

interface ImageUploaderProps {
  onImageSelected: (file: File) => void;
  selectedImage: File | null;
  imagePreviewUrl: string | null;
  onClearImage: () => void;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({
  onImageSelected,
  selectedImage,
  imagePreviewUrl,
  onClearImage,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateAndProcessFile = (file: File) => {
    setErrorMessage(null);
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type.toLowerCase())) {
      setErrorMessage('Invalid file format. Please upload a JPG, JPEG, or PNG image.');
      return;
    }
    const maxBytes = 10 * 1024 * 1024; // 10MB
    if (file.size > maxBytes) {
      setErrorMessage('File size exceeds 10MB limit. Please upload a smaller image.');
      return;
    }
    onImageSelected(file);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndProcessFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndProcessFile(e.target.files[0]);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {imagePreviewUrl ? (
        <div className="relative group rounded-3xl overflow-hidden border border-white/10 bg-slate-900/60 p-4 backdrop-blur-xl shadow-2xl transition-all">
          <div className="relative aspect-[3/4] max-h-[460px] mx-auto rounded-2xl overflow-hidden shadow-inner bg-slate-950">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={imagePreviewUrl}
              alt="Uploaded User Portrait"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end justify-center p-6">
              <button
                onClick={onClearImage}
                className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-white/20 backdrop-blur-md hover:bg-white/30 text-white font-medium text-sm transition-all shadow-lg hover:scale-105 active:scale-95"
              >
                <RefreshCw className="w-4 h-4" />
                Change Photo
              </button>
            </div>
          </div>
          <div className="mt-4 text-center flex items-center justify-between px-2">
            <span className="text-xs font-mono text-slate-400 truncate max-w-[200px]">
              {selectedImage?.name}
            </span>
            <button
              onClick={onClearImage}
              className="text-xs text-brand-400 hover:text-brand-300 font-medium underline underline-offset-4"
            >
              Upload Different Photo
            </button>
          </div>
        </div>
      ) : (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`relative cursor-pointer rounded-3xl border-2 border-dashed transition-all duration-300 p-8 sm:p-12 text-center bg-slate-900/40 backdrop-blur-xl ${
            isDragging
              ? 'border-brand-500 bg-brand-500/10 scale-[1.01]'
              : 'border-slate-700/60 hover:border-brand-400/80 hover:bg-slate-900/70'
          }`}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/jpeg,image/jpg,image/png,image/webp"
            className="hidden"
          />

          <div className="w-16 h-16 sm:w-20 sm:h-20 mx-auto mb-6 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-400 shadow-inner group-hover:scale-110 transition-transform">
            <Upload className="w-8 h-8 sm:w-10 sm:h-10" />
          </div>

          <h3 className="text-xl sm:text-2xl font-semibold text-white tracking-tight mb-2">
            Upload Your Photo
          </h3>
          <p className="text-slate-400 text-sm max-w-md mx-auto mb-6 leading-relaxed">
            Drag and drop your picture here, or browse files from your device. Supports JPG, JPEG, and PNG.
          </p>

          <div className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-gradient-to-r from-brand-600 to-brand-500 text-white font-medium text-sm shadow-lg shadow-brand-500/25 hover:shadow-brand-500/40 hover:scale-105 transition-all">
            <ImageIcon className="w-4 h-4" />
            Select Photo
          </div>

          <div className="mt-8 pt-6 border-t border-white/5 flex items-center justify-center gap-2 text-xs text-slate-400">
            <AlertCircle className="w-4 h-4 text-brand-400 shrink-0" />
            <span>For best results, upload a clear, front-facing photo with one person.</span>
          </div>
        </div>
      )}

      {errorMessage && (
        <div className="mt-4 p-4 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}
    </div>
  );
};
