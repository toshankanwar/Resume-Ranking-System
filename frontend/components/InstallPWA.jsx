'use client'

import { useState, useEffect } from 'react'
import { Download, X, Smartphone, Monitor } from 'lucide-react'

export default function InstallPWA() {
  const [deferredPrompt, setDeferredPrompt] = useState(null)
  const [isInstallable, setIsInstallable] = useState(false)
  const [isInstalled, setIsInstalled] = useState(false)
  const [showBanner, setShowBanner] = useState(false)

  useEffect(() => {
    // Check if already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true)
      return
    }

    // Listen for beforeinstallprompt event
    const handleBeforeInstallPrompt = (e) => {
      console.log('PWA: beforeinstallprompt event fired')
      e.preventDefault()
      setDeferredPrompt(e)
      setIsInstallable(true)
      
      // Show banner after 3 seconds
      setTimeout(() => {
        setShowBanner(true)
      }, 3000)
    }

    // Listen for app installed event
    const handleAppInstalled = () => {
      console.log('PWA: App was installed')
      setIsInstalled(true)
      setIsInstallable(false)
      setShowBanner(false)
      setDeferredPrompt(null)
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
    } else {
      console.log('PWA: User dismissed the install prompt')
    }

    // Clear the deferred prompt
    setDeferredPrompt(null)
    setIsInstallable(false)
  }

  const handleCloseBanner = () => {
    setShowBanner(false)
    // Show again after 1 day
    localStorage.setItem('pwa-banner-dismissed', Date.now().toString())
  }

  // Don't show if already installed
  if (isInstalled) {
    return null
  }

  // Install Button (always visible when installable)
  if (isInstallable && !showBanner) {
    return (
      <button
        onClick={handleInstallClick}
        className="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 animate-bounce-slow"
        aria-label="Install App"
      >
        <Download className="w-5 h-5" />
        <span className="font-semibold hidden sm:inline">Install App</span>
      </button>
    )
  }

  // Install Banner
  if (showBanner && isInstallable) {
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
