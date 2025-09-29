import Link from 'next/link'
import { Brain, Heart, ExternalLink } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50 mt-20">
      <div className="container py-12">
        {/* Main Footer Content */}
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          
          {/* Brand Section */}
          <div className="md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-600 to-primary-700 flex items-center justify-center">
                <Brain className="w-4 h-4 text-white" />
              </div>
              <span className="font-bold text-xl text-primary-700 dark:text-primary-400">
                ResumeRank
              </span>
            </div>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed max-w-md">
              AI-powered resume ranking system using advanced NLP and machine learning to help you find the perfect candidates efficiently and fairly.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Quick Links</h3>
            <div className="space-y-3">
              <Link href="/" className="block text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                Home
              </Link>
              <Link href="/about" className="block text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                About
              </Link>
              <Link href="/predict" className="block text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                Predict
              </Link>
              <Link href="/contact" className="block text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                Contact
              </Link>
            </div>
          </div>

          {/* Technology */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Technology</h3>
            <div className="space-y-3">
              <div className="text-sm text-gray-600 dark:text-gray-400">BERT Analysis</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Cosine Similarity</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">NER Processing</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">ML Algorithms</div>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-200 dark:border-gray-700 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            
            {/* Copyright */}
            <div className="text-sm text-gray-600 dark:text-gray-400">
              © {new Date().getFullYear()} ResumeRank. All rights reserved.
            </div>

            {/* Developer Credit */}
            <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <span>Designed and developed with</span>
              <Heart className="w-4 h-4 mx-1 text-red-500 fill-current" />
              <span>by</span>
              <Link 
                href="https://toshankanwar.website/" 
                target="_blank"
                rel="noopener noreferrer"
                className="ml-1 text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium transition-colors inline-flex items-center group"
              >
                Toshan Kanwar
                <ExternalLink className="w-3 h-3 ml-1 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
