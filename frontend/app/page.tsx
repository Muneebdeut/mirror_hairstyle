'use client';

import React, { useState, useRef } from 'react';
import {
  Sparkles,
  Scissors,
  UserCheck,
  Zap,
  ArrowRight,
  ShieldCheck,
  AlertTriangle,
  RefreshCw
} from 'lucide-react';
import { ImageUploader } from '@/components/ImageUploader';
import { FaceAnalysis } from '@/components/FaceAnalysis';
import { PreferenceSelector } from '@/components/PreferenceSelector';
import { HairstyleGrid } from '@/components/HairstyleGrid';
import { TryOnResult } from '@/components/TryOnResult';
import { LoadingState } from '@/components/LoadingState';

import {
  FaceAnalysisResult,
  HairCharacteristics,
  RecommendationItem,
  StylePreferenceType
} from '@/types';
import {
  analyzeFaceAPI,
  analyzeHairAPI,
  getRecommendationsAPI,
  requestVirtualTryOnAPI
} from '@/lib/api';

type AppStep = 'landing' | 'analyzing' | 'recommendations' | 'generating_tryon' | 'tryon_result' | 'error';

export default function Home() {
  const [currentStep, setCurrentStep] = useState<AppStep>('landing');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  // Analysis & Recommendation states
  const [faceAnalysis, setFaceAnalysis] = useState<FaceAnalysisResult | null>(null);
  const [hairTraits, setHairTraits] = useState<HairCharacteristics>({
    hair_length: 'Medium',
    hair_texture: 'Wavy',
    hair_density: 'Medium',
    hair_volume: 'Medium'
  });
  const [preference, setPreference] = useState<StylePreferenceType>('no_preference');
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [selectedHairstyle, setSelectedHairstyle] = useState<RecommendationItem | null>(null);
  const [tryOnImageUrl, setTryOnImageUrl] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const uploaderSectionRef = useRef<HTMLDivElement>(null);
  const howItWorksRef = useRef<HTMLDivElement>(null);

  const scrollToUploader = () => {
    uploaderSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const scrollToHowItWorks = () => {
    howItWorksRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Image Selection Handler
  const handleImageSelected = async (file: File) => {
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    setCurrentStep('analyzing');
    setErrorMessage(null);

    try {
      // 1. Send image for face analysis
      const analysisResult = await analyzeFaceAPI(file);
      if (!analysisResult.face_detected || analysisResult.error) {
        setErrorMessage(analysisResult.error || "We couldn't detect a face. Please upload a clear, front-facing photo.");
        setCurrentStep('error');
        return;
      }

      setFaceAnalysis(analysisResult);

      // 2. Send image for hair analysis
      const hairResult = await analyzeHairAPI(file);
      setHairTraits(hairResult);

      // 3. Fetch initial recommendations
      const recResult = await getRecommendationsAPI(
        analysisResult.face_shape || 'Oval',
        preference,
        hairResult.hair_length,
        hairResult.hair_texture
      );
      setRecommendations(recResult.recommendations);
      setCurrentStep('recommendations');
    } catch (err: any) {
      setErrorMessage(err.message || 'An error occurred during facial analysis.');
      setCurrentStep('error');
    }
  };

  // Preference Change Handler
  const handlePreferenceChange = async (newPref: StylePreferenceType) => {
    setPreference(newPref);
    if (faceAnalysis?.face_shape) {
      const recResult = await getRecommendationsAPI(
        faceAnalysis.face_shape,
        newPref,
        hairTraits.hair_length,
        hairTraits.hair_texture
      );
      setRecommendations(recResult.recommendations);
    }
  };

  // Face Shape Edit Handler
  const handleFaceShapeChange = async (newShape: string) => {
    if (faceAnalysis) {
      setFaceAnalysis({ ...faceAnalysis, face_shape: newShape });
      const recResult = await getRecommendationsAPI(
        newShape,
        preference,
        hairTraits.hair_length,
        hairTraits.hair_texture
      );
      setRecommendations(recResult.recommendations);
    }
  };

  // Hair Traits Edit Handler
  const handleUpdateHairTraits = async (updated: HairCharacteristics) => {
    setHairTraits(updated);
    if (faceAnalysis?.face_shape) {
      const recResult = await getRecommendationsAPI(
        faceAnalysis.face_shape,
        preference,
        updated.hair_length,
        updated.hair_texture
      );
      setRecommendations(recResult.recommendations);
    }
  };

  // Select Hairstyle for Virtual Try-On
  const handleSelectHairstyle = async (item: RecommendationItem) => {
    if (!selectedFile) return;
    setSelectedHairstyle(item);
    setCurrentStep('generating_tryon');

    try {
      const res = await requestVirtualTryOnAPI(
        selectedFile,
        item.hairstyle.name,
        item.hairstyle.prompt_hint || ''
      );
      if (res.success && res.tryon_image_url) {
        setTryOnImageUrl(res.tryon_image_url);
        setCurrentStep('tryon_result');
      } else {
        throw new Error(res.message || 'Failed to generate virtual try-on preview.');
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to generate virtual try-on preview.');
      setCurrentStep('error');
    }
  };

  // Reset Application State
  const handleStartOver = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setFaceAnalysis(null);
    setRecommendations([]);
    setSelectedHairstyle(null);
    setTryOnImageUrl(null);
    setErrorMessage(null);
    setCurrentStep('landing');
  };

  return (
    <div className="min-h-screen flex flex-col justify-between bg-slate-950 text-slate-100 selection:bg-brand-500 selection:text-white">
      {/* Top Header / Navigation Bar */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-slate-950/80 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          <div
            onClick={handleStartOver}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-brand-600 to-brand-400 flex items-center justify-center text-white shadow-lg shadow-brand-500/25 group-hover:scale-105 transition-transform">
              <Scissors className="w-5 h-5" />
            </div>
            <span className="text-xl font-extrabold tracking-tight text-white group-hover:text-brand-300 transition-colors">
              AI Hairstyle<span className="text-brand-400">Advisor</span>
            </span>
          </div>

          <div className="flex items-center gap-4">
            {currentStep !== 'landing' && (
              <button
                onClick={handleStartOver}
                className="flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-medium text-slate-300 hover:text-white transition-all"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                Start Over
              </button>
            )}
            <button
              onClick={scrollToUploader}
              className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-gradient-to-r from-brand-600 to-brand-500 hover:from-brand-500 hover:to-brand-400 text-white font-bold text-xs shadow-md shadow-brand-500/20 hover:scale-105 transition-all"
            >
              <Sparkles className="w-4 h-4" />
              Try It Now
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-16">
        {/* STEP 1: LANDING & HERO SECTION */}
        {(currentStep === 'landing' || currentStep === 'analyzing') && (
          <div className="space-y-16">
            {/* Hero Banner */}
            <div className="relative pt-12 pb-8 text-center space-y-8 max-w-4xl mx-auto">
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-brand-500/15 rounded-full blur-3xl pointer-events-none" />

              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs font-bold uppercase tracking-wider shadow-inner">
                <Sparkles className="w-4 h-4 text-gold-400" />
                Next-Gen Computer Vision & AI Try-On
              </div>

              <h1 className="text-4xl sm:text-6xl lg:text-7xl font-black text-white tracking-tight leading-none">
                Find Your Perfect Hairstyle with <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 via-white to-gold-400">AI</span>
              </h1>

              <p className="text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto leading-relaxed">
                Upload your photo, discover hairstyles that complement your facial features, and see yourself with a new look using AI virtual try-on.
              </p>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                <button
                  onClick={scrollToUploader}
                  className="w-full sm:w-auto flex items-center justify-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-brand-600 via-brand-500 to-brand-600 hover:from-brand-500 hover:to-brand-400 text-white font-extrabold text-base shadow-xl shadow-brand-500/30 hover:scale-105 active:scale-95 transition-all"
                >
                  <Sparkles className="w-5 h-5" />
                  Try It Now
                  <ArrowRight className="w-5 h-5" />
                </button>

                <button
                  onClick={scrollToHowItWorks}
                  className="w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-4 rounded-2xl bg-slate-900 border border-white/10 hover:bg-slate-850 hover:border-white/20 text-slate-300 hover:text-white font-bold text-base transition-all"
                >
                  How It Works
                </button>
              </div>

              {/* Before -> AI -> After Visual Demonstration */}
              <div className="pt-8">
                <div className="inline-flex items-center justify-center gap-3 sm:gap-6 px-6 py-3 rounded-2xl bg-slate-900/60 border border-white/10 backdrop-blur-md text-xs sm:text-sm font-semibold text-slate-300 shadow-xl">
                  <span className="text-slate-400 uppercase tracking-wider">Before</span>
                  <ArrowRight className="w-4 h-4 text-brand-400" />
                  <span className="px-3 py-1 rounded-full bg-brand-500/20 text-brand-300 font-bold uppercase tracking-wider">AI Hairstyle Analysis</span>
                  <ArrowRight className="w-4 h-4 text-brand-400" />
                  <span className="text-gold-400 font-bold uppercase tracking-wider">After Preview</span>
                </div>
              </div>
            </div>

            {/* Photo Uploader Card */}
            <div ref={uploaderSectionRef} className="pt-4 scroll-mt-28">
              {currentStep === 'analyzing' ? (
                <LoadingState
                  title="Analyzing Facial Landmark Features..."
                  subtitle="MediaPipe 3D face mesh is calculating facial proportions and estimating your face shape."
                  step="Running computer vision landmark analysis"
                />
              ) : (
                <ImageUploader
                  onImageSelected={handleImageSelected}
                  selectedImage={selectedFile}
                  imagePreviewUrl={previewUrl}
                  onClearImage={handleStartOver}
                />
              )}
            </div>

            {/* "How It Works" Section */}
            <div ref={howItWorksRef} className="pt-16 border-t border-white/10 scroll-mt-28 space-y-12">
              <div className="text-center space-y-3">
                <h2 className="text-3xl font-extrabold text-white tracking-tight">How It Works</h2>
                <p className="text-slate-400 text-sm max-w-lg mx-auto">
                  Experience seamless AI fashion styling in 4 simple steps.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="rounded-3xl bg-slate-900/50 border border-white/10 p-6 space-y-4">
                  <div className="w-12 h-12 rounded-2xl bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center font-bold text-lg">
                    1
                  </div>
                  <h3 className="text-lg font-bold text-white">Upload Your Photo</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    Upload a clear, front-facing portrait photo from your phone or device.
                  </p>
                </div>

                <div className="rounded-3xl bg-slate-900/50 border border-white/10 p-6 space-y-4">
                  <div className="w-12 h-12 rounded-2xl bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center font-bold text-lg">
                    2
                  </div>
                  <h3 className="text-lg font-bold text-white">AI Analyzes Features</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    Computer vision measures forehead, cheekbones, and jaw geometric ratios to estimate face shape.
                  </p>
                </div>

                <div className="rounded-3xl bg-slate-900/50 border border-white/10 p-6 space-y-4">
                  <div className="w-12 h-12 rounded-2xl bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center font-bold text-lg">
                    3
                  </div>
                  <h3 className="text-lg font-bold text-white">Discover Hairstyles</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    Our recommendation engine ranks top hairstyles matching your proportions and style preferences.
                  </p>
                </div>

                <div className="rounded-3xl bg-slate-900/50 border border-white/10 p-6 space-y-4">
                  <div className="w-12 h-12 rounded-2xl bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center font-bold text-lg">
                    4
                  </div>
                  <h3 className="text-lg font-bold text-white">Try Your New Look</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    Generate an interactive before/after preview of your selected hairstyle directly on your photo.
                  </p>
                </div>
              </div>
            </div>

            {/* Feature Highlights Section */}
            <div className="pt-12 border-t border-white/10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="flex items-start gap-4 p-5 rounded-2xl bg-slate-900/30 border border-white/5">
                <div className="p-3 rounded-xl bg-brand-500/10 text-brand-400 shrink-0">
                  <UserCheck className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-bold text-white text-base">AI Face Analysis</h4>
                  <p className="text-xs text-slate-400 mt-1">Precise landmark-based face shape estimation.</p>
                </div>
              </div>

              <div className="flex items-start gap-4 p-5 rounded-2xl bg-slate-900/30 border border-white/5">
                <div className="p-3 rounded-xl bg-brand-500/10 text-brand-400 shrink-0">
                  <Sparkles className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-bold text-white text-base">Personalized Recommendations</h4>
                  <p className="text-xs text-slate-400 mt-1">Tailored hairstyle compatibility scoring.</p>
                </div>
              </div>

              <div className="flex items-start gap-4 p-5 rounded-2xl bg-slate-900/30 border border-white/5">
                <div className="p-3 rounded-xl bg-brand-500/10 text-brand-400 shrink-0">
                  <Zap className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-bold text-white text-base">Virtual Hairstyle Try-On</h4>
                  <p className="text-xs text-slate-400 mt-1">Photorealistic before & after slider preview.</p>
                </div>
              </div>

              <div className="flex items-start gap-4 p-5 rounded-2xl bg-slate-900/30 border border-white/5">
                <div className="p-3 rounded-xl bg-brand-500/10 text-brand-400 shrink-0">
                  <Scissors className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-bold text-white text-base">Multiple Style Preferences</h4>
                  <p className="text-xs text-slate-400 mt-1">Explore Masculine, Feminine, Unisex & No Preference.</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* STEP 2: RECOMMENDATIONS & ANALYSIS RESULT */}
        {currentStep === 'recommendations' && faceAnalysis && (
          <div className="space-y-12 animate-fadeIn">
            {/* Face & Hair Analysis Section */}
            <FaceAnalysis
              analysis={faceAnalysis}
              hairCharacteristics={hairTraits}
              onUpdateHairCharacteristics={handleUpdateHairTraits}
              onUpdateFaceShape={handleFaceShapeChange}
            />

            {/* Style Preference Selector */}
            <PreferenceSelector
              selectedPreference={preference}
              onChangePreference={handlePreferenceChange}
            />

            {/* Recommended Hairstyle Grid */}
            <HairstyleGrid
              recommendations={recommendations}
              onSelectHairstyle={handleSelectHairstyle}
              selectedHairstyle={selectedHairstyle}
            />
          </div>
        )}

        {/* STEP 3: TRY-ON GENERATION LOADING */}
        {currentStep === 'generating_tryon' && (
          <LoadingState
            title={`Generating AI Virtual Try-On for ${selectedHairstyle?.name}...`}
            subtitle="Preserving facial identity, skin tone, background, and rendering realistic hair strands."
            step="Applying AI virtual try-on edit"
          />
        )}

        {/* STEP 4: BEFORE / AFTER VIRTUAL TRY-ON RESULT */}
        {currentStep === 'tryon_result' && previewUrl && tryOnImageUrl && selectedHairstyle && (
          <TryOnResult
            originalImageUrl={previewUrl}
            tryOnImageUrl={tryOnImageUrl}
            selectedHairstyle={selectedHairstyle}
            onTryAnother={() => setCurrentStep('recommendations')}
            onStartOver={handleStartOver}
          />
        )}

        {/* STEP 5: ERROR STATE */}
        {currentStep === 'error' && (
          <div className="max-w-md mx-auto p-8 rounded-3xl bg-slate-900/90 border border-rose-500/30 text-center space-y-6 animate-fadeIn">
            <div className="w-16 h-16 mx-auto rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center justify-center">
              <AlertTriangle className="w-8 h-8" />
            </div>
            <div className="space-y-2">
              <h3 className="text-xl font-bold text-white">Analysis Could Not Proceed</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                {errorMessage || "We couldn't process the photo. Please ensure your photo is clear and contains exactly one face."}
              </p>
            </div>
            <button
              onClick={handleStartOver}
              className="w-full py-3.5 px-6 rounded-2xl bg-gradient-to-r from-brand-600 to-brand-500 text-white font-bold text-sm shadow-lg shadow-brand-500/25 hover:scale-105 transition-all"
            >
              Upload Different Photo
            </button>
          </div>
        )}
      </main>

      {/* Footer & Privacy Note */}
      <footer className="border-t border-white/10 bg-slate-950 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-3">
          <div className="flex items-center justify-center gap-2 text-xs text-slate-400">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Privacy Note: Your photo is used only to analyze your hairstyle and generate your preview.</span>
          </div>
          <p className="text-xs text-slate-500">
            © {new Date().getFullYear()} AI Hairstyle Advisor. Production Quality MVP.
          </p>
        </div>
      </footer>
    </div>
  );
}
