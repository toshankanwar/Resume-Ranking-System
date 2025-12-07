'use client'

import { useState, useEffect } from 'react'
import { Download, X, Smartphone } from 'lucide-react'

const BANNER_DISMISSED_KEY = 'pwa-banner-dismissed'

export default function InstallPWA() {
  const [deferredPrompt, setDeferredPrompt] = useState(null)
  const [isInstallable, setIsInstallable] = useState(false)
  const [isInstalled, setIsInstalled] = useState(false)
  const [showBanner, setShowBanner] = useState(false)
  const [bannerDismissed, setBannerDismissed] = useState(false)

  useEffect(() => {
    if (typeof window === 'undefined') return

    // Check if already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true)
      return
    }

    // Check if banner was previously dismissed
    const dismissed = localStorage.getItem(BANNER_DISMISSED_KEY)
    if (dismissed) {
      setBannerDismissed(true)
    }

    // Listen for beforeinstallprompt event
    const handleBeforeInstallPrompt = (e) => {
      console.log('PWA: beforeinstallprompt event fired')
      e.preventDefault()
      setDeferredPrompt(e)
      setIsInstallable(true)
      
      // Only show banner if not previously dismissed
      if (!dismissed) {
        setTimeout(() => {
          setShowBanner(true)
        }, 3000)
      }
    }

    // Listen for app installed event
    const handleAppInstalled = () => {
      console.log('PWA: App was installed')
      setIsInstalled(true)
      setIsInstallable(false)
      setShowBanner(false)
      setDeferredPrompt(null)
      localStorage.setItem(BANNER_DISMISSED_KEY, 'installed')
    }

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
    window.addEventListener('appinstalled', handleAppInstalled)

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
      window.removeEventListener('appinstalled', handleAppInstalled)
    }
  }, [])

  const handleInstallClick = async () => {
    if (!deferredPrompt) {
      console.log('PWA: No deferred prompt available')
      return
    }

    // Show the install prompt
    deferredPrompt.prompt()

    // Wait for the user's response
    const { outcome } = await deferredPrompt.userChoice
    console.log(`PWA: User response: ${outcome}`)

    if (outcome === 'accepted') {
      console.log('PWA: User accepted the install prompt')
      setShowBanner(false)
      localStorage.setItem(BANNER_DISMISSED_KEY, 'accepted')
    } else {
      console.log('PWA: User dismissed the install prompt')
      // User declined but keep floating button visible
      setShowBanner(false)
      setBannerDismissed(true)
      localStorage.setItem(BANNER_DISMISSED_KEY, 'declined')
    }

    // Clear the deferred prompt
    setDeferredPrompt(null)
    setIsInstallable(false)
  }

  const handleCloseBanner = () => {
    console.log('PWA: User closed banner')
    setShowBanner(false)
    setBannerDismissed(true)
    // Mark banner as dismissed permanently
    localStorage.setItem(BANNER_DISMISSED_KEY, 'closed')
  }

  // Don't show anything if already installed
  if (isInstalled) {
    return null
  }

  // Show floating install button if installable and banner was dismissed or not shown
  if (isInstallable && !showBanner && deferredPrompt) {
    return (
      <button
        onClick={handleInstallClick}
        className="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
        aria-label="Install App"
        title="Install ResumeRank PWA"
      >
        <Download className="w-5 h-5" />
        <span className="font-semibold hidden sm:inline">Install App</span>
      </button>
    )
  }

  // Show banner only if not dismissed before
  if (showBanner && isInstallable && !bannerDismissed) {
    return (
      <div className="fixed bottom-0 left-0 right-0 z-50 p-4 bg-gradient-to-r from-primary-600 via-purple-600 to-primary-700 text-white shadow-2xl animate-slide-up">
        <div className="container mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center justify-center w-12 h-12 bg-white/20 rounded-xl backdrop-blur-sm">
              <Smartphone className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-lg">Install ResumeRank</h3>
              <p className="text-sm text-primary-100">
                Install our app for a better experience and offline access
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleInstallClick}
              className="flex items-center gap-2 px-6 py-3 bg-white text-primary-700 rounded-xl font-bold hover:bg-primary-50 transition-colors"
            >
              <Download className="w-5 h-5" />
              <span className="hidden sm:inline">Install</span>
            </button>
            <button
              onClick={handleCloseBanner}
              className="p-2 hover:bg-white/20 rounded-lg transition-colors"
              aria-label="Close"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    )
  }

  return null
}
