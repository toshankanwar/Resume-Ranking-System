export default function manifest() {
    // You can add Firebase config here if needed
    const isProd = process.env.NODE_ENV === 'production'
    
    return {
      name: 'ResumeRank - AI-Powered Resume Ranking',
      short_name: 'ResumeRank',
      description: 'AI-powered resume screening and ranking system using BERT, NLP, and machine learning',
      start_url: '/',
      display: 'standalone',
      background_color: '#ffffff',
      theme_color: '#6366f1',
      orientation: 'portrait-primary',
      scope: '/',
      icons: [
        {
          src: '/icon-192x192.png',
          sizes: '192x192',
          type: 'image/png',
          purpose: 'any maskable'
        },
        {
          src: '/icon-512x512.png',
          sizes: '512x512',
          type: 'image/png',
          purpose: 'any maskable'
        },
        {
          src: '/icon-192x192.png',
          sizes: '192x192',
          type: 'image/png',
          purpose: 'maskable'
        }
      ],
      categories: ['business', 'productivity', 'utilities'],
      screenshots: [
        {
          src: '/screenshot-wide.png',
          sizes: '1280x720',
          type: 'image/png',
          form_factor: 'wide',
          label: 'Resume Analysis Dashboard'
        },
        {
          src: '/screenshot-mobile.png',
          sizes: '750x1334',
          type: 'image/png',
          form_factor: 'narrow',
          label: 'Mobile View'
        }
      ]
    }
  }
  