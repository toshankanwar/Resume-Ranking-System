'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Brain } from 'lucide-react'
import ThemeToggle from './ThemeToggle'

export default function Header() {
  const pathname = usePathname()

  return (
    <header className="border-b border-gray-200 dark:border-gray-800 bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm sticky top-0 z-50">
      <div className="container py-4">
        <div className="flex items-center justify-between">
          
          {/* Enhanced Logo */}
          <Link href="/" className="flex items-center space-x-2 group">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-600 to-primary-700 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <Brain className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-xl text-primary-700 dark:text-primary-400 group-hover:text-primary-600 dark:group-hover:text-primary-300 transition-colors">
              ResumeRank
            </span>
          </Link>
          
          {/* Enhanced Navigation - Now in Middle */}
          <nav className="flex items-center gap-2">
            <Link 
              href="/" 
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                pathname === '/' 
                  ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300' 
                  : 'text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-800/50'
              }`}
            >
              Home
            </Link>
            <Link 
              href="/about" 
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                pathname === '/about' 
                  ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300' 
                  : 'text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-800/50'
              }`}
            >
              About
            </Link>
            <Link 
              href="/predict" 
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                pathname === '/predict' 
                  ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300' 
                  : 'text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-800/50'
              }`}
            >
              Predict
            </Link>
            <Link 
              href="/contact" 
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                pathname === '/contact' 
                  ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300' 
                  : 'text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-800/50'
              }`}
            >
              Contact
            </Link>
          </nav>
          
          {/* Theme Toggle with same height */}
          <ThemeToggle />
          
        </div>
      </div>
    </header>
  )
}
