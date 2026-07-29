import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Hairstyle Advisor | Discover & Virtual Try-On Hairstyles',
  description: 'Upload your photo, analyze your facial landmarks & face shape, get personalized hairstyle recommendations, and preview your new look with AI virtual try-on.',
  keywords: ['AI Hairstyle', 'Virtual Try-On', 'Face Shape Analysis', 'Beauty AI', 'Hairstyle Recommendation'],
  openGraph: {
    title: 'AI Hairstyle Advisor',
    description: 'Find your perfect hairstyle with computer vision and AI virtual try-on.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between">
        {children}
      </body>
    </html>
  );
}
