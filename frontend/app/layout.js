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

// Dynamic base URL
const baseUrl = process.env.VERCEL_URL 
  ? `https://${process.env.VERCEL_URL}`
  : process.env.NODE_ENV === 'production'
    ? 'https://resume.createfast.tech'
    : 'http://localhost:3000'

export const metadata = {
  metadataBase: new URL(baseUrl), // ✅ Added for Vercel
  
  title: {
    default: 'ResumeRank - AI-Powered Resume Ranking System | Smart Recruitment Software',
    template: '%s | ResumeRank - AI Resume Screening'
  },
  
  description: 'AI-powered resume screening and ranking system using BERT, NLP, and machine learning. Analyze resumes in seconds with 92.5% accuracy. Automate your recruitment process with intelligent candidate ranking.',
  
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
    'recruitment software',
    'ATS system',
    'applicant tracking',
    'resume analyzer',
    'CV screening',
    'talent acquisition',
    'HR automation',
    'resume matching',
    'job candidate screening'
  ],
  
  authors: [
    { name: 'Toshan Kanwar', url: 'https://toshankanwar.website' }
  ],
  creator: 'Toshan Kanwar',
  publisher: 'ResumeRank',
  
  // Referrer policy
  referrer: 'origin-when-cross-origin',
  
  // Open Graph (Facebook, LinkedIn, Discord, WhatsApp)
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: baseUrl,
    siteName: 'ResumeRank',
    title: 'ResumeRank - AI-Powered Resume Ranking System',
    description: 'AI-powered resume screening using BERT, NLP, and machine learning. Analyze 10,000+ resumes with 92.5% accuracy. Automate your recruitment with smart candidate ranking.',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'ResumeRank - AI Resume Ranking Dashboard',
        type: 'image/png',
      },
      {
        url: '/og-image-square.png',
        width: 1200,
        height: 1200,
        alt: 'ResumeRank Logo - AI Recruitment Software',
        type: 'image/png',
      }
    ],
  },
  
  // Twitter Card
  twitter: {
    card: 'summary_large_image',
    title: 'ResumeRank - AI-Powered Resume Ranking & Screening',
    description: 'AI-powered resume screening using BERT, NLP, and ML. Analyze resumes with 92.5% accuracy. Automate recruitment.',
    site: '@toshankanwar',
    creator: '@toshankanwar',
    images: {
      url: '/og-image.png',
      alt: 'ResumeRank AI Resume Screening Dashboard',
    },
  },
  
  // Robots
  robots: {
    index: true,
    follow: true,
    nocache: false,
    googleBot: {
      index: true,
      follow: true,
      noimageindex: false,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  
  // Alternate languages (if you have multi-language)
  alternates: {
    canonical: baseUrl,
    languages: {
      'en-US': baseUrl,
      // Add more if needed
      // 'hi-IN': `${baseUrl}/hi`,
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
  
  // Manifest
  manifest: '/manifest.json',
  
  // App Links (for deep linking)
  appLinks: {
    web: {
      url: baseUrl,
      should_fallback: true,
    },
  },
  
  // Archives (for sitemap)
  archives: [`${baseUrl}/sitemap.xml`],
  
  // Assets
  assets: [`${baseUrl}/assets`],
  
  // Bookmarks
  bookmarks: [baseUrl],
  
  // Category
  category: 'technology',
  classification: 'Business Software',
  
  // Other Meta
  other: {
    'mobile-web-app-capable': 'yes',
    'apple-mobile-web-app-capable': 'yes',
    'application-name': 'ResumeRank',
    'msapplication-TileColor': '#6366f1',
    'msapplication-config': '/browserconfig.xml',
    'theme-color': '#6366f1',
  },
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
  colorScheme: 'light dark',
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
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta property="og:image:type" content="image/png" />
        
        {/* Twitter Additional Tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:site" content="@toshankanwar" />
        <meta name="twitter:creator" content="@toshankanwar" />
        <meta name="twitter:image:alt" content="ResumeRank AI Resume Screening Dashboard" />
        
        {/* Microsoft Tags */}
        <meta name="msapplication-TileColor" content="#6366f1" />
        <meta name="msapplication-TileImage" content="/mstile-150x150.png" />
        <meta name="msapplication-config" content="/browserconfig.xml" />
        <meta name="msapplication-tap-highlight" content="no" />
        <meta name="msapplication-navbutton-color" content="#6366f1" />
        <meta name="msapplication-starturl" content="/" />
        
        {/* Additional Meta for SEO */}
        <meta name="format-detection" content="telephone=no" />
        <meta name="format-detection" content="date=no" />
        <meta name="format-detection" content="address=no" />
        <meta name="format-detection" content="email=no" />
        <meta name="rating" content="General" />
        <meta name="distribution" content="Global" />
        <meta name="language" content="English" />
        <meta name="revisit-after" content="7 days" />
        <meta name="author" content="Toshan Kanwar" />
        <meta name="copyright" content="ResumeRank" />
        <meta name="coverage" content="Worldwide" />
        <meta name="target" content="all" />
        <meta name="HandheldFriendly" content="True" />
        <meta name="MobileOptimized" content="320" />
        
        {/* Preconnect for Performance */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://firebasestorage.googleapis.com" />
        
        {/* Schema.org JSON-LD */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'SoftwareApplication',
              name: 'ResumeRank',
              applicationCategory: 'BusinessApplication',
              operatingSystem: 'Web, Android, iOS',
              offers: {
                '@type': 'Offer',
                price: '0',
                priceCurrency: 'USD',
              },
              aggregateRating: {
                '@type': 'AggregateRating',
                ratingValue: '4.8',
                ratingCount: '250',
              },
              description: 'AI-powered resume screening and ranking system using BERT, NLP, and machine learning.',
              author: {
                '@type': 'Person',
                name: 'Toshan Kanwar',
                url: 'https://toshankanwar.website',
              },
              publisher: {
                '@type': 'Organization',
                name: 'ResumeRank',
                logo: {
                  '@type': 'ImageObject',
                  url: `${baseUrl}/icon-512x512.png`,
                },
              },
              screenshot: `${baseUrl}/og-image.png`,
              softwareVersion: '1.0.0',
              datePublished: '2024-01-01',
              dateModified: new Date().toISOString(),
            }),
          }}
        />
        
        {/* Organization Schema */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'Organization',
              name: 'ResumeRank',
              url: baseUrl,
              logo: `${baseUrl}/icon-512x512.png`,
              description: 'AI-powered resume screening and ranking system',
              foundingDate: '2024',
              founder: {
                '@type': 'Person',
                name: 'Toshan Kanwar',
              },
              contactPoint: {
                '@type': 'ContactPoint',
                contactType: 'Customer Support',
                email: 'support@resume.createfast.tech',
              },
              sameAs: [
                'https://github.com/yourusername',
                'https://linkedin.com/in/yourusername',
              ],
            }),
          }}
        />
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
