'use client'

import { useState, useEffect } from 'react'
import { Copy, Check } from 'lucide-react'

export default function ShareButton({ 
  className = ''
}) {
  const [copied, setCopied] = useState(false)
  const [appUrl, setAppUrl] = useState('')

  // Set PWA URL on client side
  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Get base URL (homepage)
      const baseUrl = `${window.location.protocol}//${window.location.host}`
      setAppUrl(baseUrl)
    }
  }, [])

  // Copy PWA install link to clipboard
  const handleCopyLink = async () => {
    const shareText = `Install ResumeRank PWA: ${appUrl}\n\n🚀 AI-powered resume ranking system\n📱 Works offline\n⚡ Install as app on any device`
    
    try {
      await navigator.clipboard.writeText(shareText)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy:', error)
      // Fallback for older browsers
      const textArea = document.createElement('textarea')
      textArea.value = shareText
      textArea.style.position = 'fixed'
      textArea.style.left = '-9999px'
      document.body.appendChild(textArea)
      textArea.select()
      try {
        document.execCommand('copy')
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      } catch (err) {
        console.error('Fallback copy failed:', err)
      }
      document.body.removeChild(textArea)
    }
  }

  return (
    <button
      onClick={handleCopyLink}
      className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
        copied 
          ? 'bg-green-600 hover:bg-green-700 text-white'
          : 'bg-primary-600 hover:bg-primary-700 text-white'
      } ${className}`}
      aria-label="Copy PWA link"
      title="Copy app install link"
    >
      {copied ? (
        <>
          <Check className="w-5 h-5" />
          <span className="hidden sm:inline">Copied!</span>
        </>
      ) : (
        <>
          <Copy className="w-5 h-5" />
          <span className="hidden sm:inline">Share App</span>
        </>
      )}
    </button>
  )
}
