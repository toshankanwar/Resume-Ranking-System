import './globals.css'
import { Inter } from 'next/font/google'
import { ThemeProvider } from '../components/ThemeProvider'
import Header from '../components/Header'
import Footer from '../components/Footer'
import InstallPWA from '../components/InstallPWA'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
})

export const metadata = {
  title: {
    default: 'ResumeRank - AI-Powered Resume Ranking System',
    template: '%s | ResumeRank'
  },
  description: 'AI-powered resume screening and ranking system using BERT, NLP, and machine learning. Analyze resumes in seconds with 92.5% accuracy.',
  applicationName: 'ResumeRank',
  
  // Keywords for SEO
  keywords: [
    'resume ranking',
    'AI resume screening',
    'BERT resume analysis',
    'resume parser',
    'NLP resume',
    'machine learning recruitment',
    'automated resume screening',
    'candidate ranking',
    'resume AI',
    'recruitment software'
  ],
  
  authors: [
    { name: 'Toshan Kanwar', url: 'https://toshankanwar.website' }
  ],
  creator: 'Toshan Kanwar',
  publisher: 'ResumeRank',
  
  // Open Graph (Facebook, LinkedIn, Discord)
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://yoursite.com', // Replace with your actual domain
    siteName: 'ResumeRank',
    title: 'ResumeRank - AI-Powered Resume Ranking System',
    description: 'AI-powered resume screening using BERT, NLP, and machine learning. Analyze 10,000+ resumes with 92.5% accuracy.',
    images: [
      {
        url: '/og-image.png', // 1200x630px
        width: 1200,
        height: 630,
        alt: 'ResumeRank - AI Resume Ranking Dashboard',
        type: 'image/png',
      },
      {
        url: '/og-image-square.png', // 1200x1200px for Instagram
        width: 1200,
        height: 1200,
        alt: 'ResumeRank Logo',
        type: 'image/png',
      }
    ],
  },
  
  // Twitter Card
  twitter: {
    card: 'summary_large_image',
    title: 'ResumeRank - AI-Powered Resume Ranking',
    description: 'AI-powered resume screening using BERT, NLP, and ML. 92.5% accuracy.',
    site: '@yourhandle', // Replace with your Twitter handle
    creator: '@yourhandle',
    images: ['/og-image.png'],
  },
  
  // Robots
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  
  // Apple Web App
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'ResumeRank',
    startupImage: [
      {
        url: '/apple-splash-2048-2732.png',
        media: '(device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2)',
      },
      {
        url: '/apple-splash-1668-2388.png',
        media: '(device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2)',
      },
      {
        url: '/apple-splash-1536-2048.png',
        media: '(device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2)',
      },
      {
        url: '/apple-splash-1125-2436.png',
        media: '(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)',
      },
      {
        url: '/apple-splash-1242-2688.png',
        media: '(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3)',
      },
      {
        url: '/apple-splash-828-1792.png',
        media: '(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2)',
      },
      {
        url: '/apple-splash-1242-2208.png',
        media: '(device-width: 414px) and (device-height: 736px) and (-webkit-device-pixel-ratio: 3)',
      },
      {
        url: '/apple-splash-750-1334.png',
        media: '(device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2)',
      },
      {
        url: '/apple-splash-640-1136.png',
        media: '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)',
      },
    ],
  },
  
  // Format Detection
  formatDetection: {
    telephone: false,
    email: false,
    address: false,
  },
  
  // Icons
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/icon-192x192.png', sizes: '192x192', type: 'image/png' },
      { url: '/icon-512x512.png', sizes: '512x512', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
    other: [
      {
        rel: 'mask-icon',
        url: '/safari-pinned-tab.svg',
        color: '#6366f1',
      },
    ],
  },
  
  // Verification (Add your verification codes)
  verification: {
    google: 'your-google-verification-code',
    yandex: 'your-yandex-verification-code',
    // yahoo: 'your-yahoo-verification-code',
    // other: 'your-other-verification-code',
  },
  
  // Other Meta
  category: 'technology',
  classification: 'Business Software',
}

export const viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#6366f1' },
    { media: '(prefers-color-scheme: dark)', color: '#4f46e5' }
  ],
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  viewportFit: 'cover',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        {/* PWA Meta Tags */}
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="ResumeRank" />
        <meta name="mobile-web-app-capable" content="yes" />
        
        {/* Additional OG Tags */}
        <meta property="og:site_name" content="ResumeRank" />
        <meta property="og:locale" content="en_US" />
        <meta property="og:type" content="website" />
        
        {/* Twitter Additional Tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:site" content="@yourhandle" />
        <meta name="twitter:creator" content="@yourhandle" />
        
        {/* Microsoft Tags */}
        <meta name="msapplication-TileColor" content="#6366f1" />
        <meta name="msapplication-config" content="/browserconfig.xml" />
        <meta name="msapplication-tap-highlight" content="no" />
        
        {/* Additional Meta */}
        <meta name="format-detection" content="telephone=no" />
        <meta name="format-detection" content="date=no" />
        <meta name="format-detection" content="address=no" />
        <meta name="format-detection" content="email=no" />
        
        {/* Preconnect for Performance */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
        
        {/* Canonical URL */}
        <link rel="canonical" href="https://yoursite.com" />
      </head>
      <body className={inter.className}>
        <ThemeProvider>
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 flex flex-col">
            <Header />
            <main className="flex-grow">
              {children}
            </main>
            <Footer />
            <InstallPWA />
          </div>
        </ThemeProvider>
      </body>
    </html>
  )
}
