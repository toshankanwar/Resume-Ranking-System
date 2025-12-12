import Link from 'next/link'
import { Brain, Heart, ExternalLink, Mail, Linkedin, Github, Twitter } from 'lucide-react'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  const quickLinks = [
    { href: '/', label: 'Home' },
    { href: '/about', label: 'About' },
    { href: '/predict', label: 'Predict' },
    { href: '/contact', label: 'Contact' },
  ]

  const technologies = [
    'BERT Analysis',
    'DistilBERT',
    'S-BERT',
    'Cosine Similarity',
    'NER Processing',
    'XGBoost ML',
  ]

  const legalLinks = [
    { href: '/privacy', label: 'Privacy Policy' },
    { href: '/terms', label: 'Terms of Service' },
    { href: '/cookies', label: 'Cookie Policy' },
  ]

  return (
    <footer className="border-t border-gray-200 dark:border-gray-800 bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-950 mt-20">
      <div className="container">
        {/* Main Footer Content */}
        <div className="py-12 lg:py-16">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12">
            
            {/* Brand Section */}
            <div className="sm:col-span-2 lg:col-span-1">
              <Link href="/" className="inline-flex items-center space-x-2 mb-4 group">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-600 to-primary-700 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <span className="font-bold text-2xl text-primary-700 dark:text-primary-400">
                  ResumeRank
                </span>
              </Link>
              <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed mb-6">
                AI-powered resume ranking system using advanced NLP and machine learning to help you find the perfect candidates efficiently and fairly.
              </p>
              
              {/* Social Links */}
              <div className="flex items-center gap-3">
                <a
                  href="https://twitter.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-primary-100 dark:hover:bg-primary-900/30 hover:text-primary-600 dark:hover:text-primary-400 transition-all duration-300"
                  aria-label="Twitter"
                >
                  <Twitter className="w-4 h-4" />
                </a>
                <a
                  href="https://www.linkedin.com/in/toshan-kanwar-4683a1349/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-primary-100 dark:hover:bg-primary-900/30 hover:text-primary-600 dark:hover:text-primary-400 transition-all duration-300"
                  aria-label="LinkedIn"
                >
                  <Linkedin className="w-4 h-4" />
                </a>
                <a
                  href="https://github.com/toshankanwar"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-primary-100 dark:hover:bg-primary-900/30 hover:text-primary-600 dark:hover:text-primary-400 transition-all duration-300"
                  aria-label="GitHub"
                >
                  <Github className="w-4 h-4" />
                </a>
                <a
                  href="mailto:contact@toshankanwar.in"
                  className="w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-primary-100 dark:hover:bg-primary-900/30 hover:text-primary-600 dark:hover:text-primary-400 transition-all duration-300"
                  aria-label="Email"
                >
                  <Mail className="w-4 h-4" />
                </a>
              </div>
            </div>

            {/* Quick Links */}
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4 text-sm uppercase tracking-wider">
                Quick Links
              </h3>
              <ul className="space-y-3">
                {quickLinks.map(link => (
                  <li key={link.href}>
                    <Link 
                      href={link.href} 
                      className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors inline-flex items-center group"
                    >
                      <span className="group-hover:translate-x-1 transition-transform duration-200">
                        {link.label}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Technology */}
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4 text-sm uppercase tracking-wider">
                Technology
              </h3>
              <ul className="space-y-3">
                {technologies.map((tech, index) => (
                  <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-center">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary-500 mr-2"></div>
                    {tech}
                  </li>
                ))}
              </ul>
            </div>

            {/* Legal & Support */}
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4 text-sm uppercase tracking-wider">
                Legal & Support
              </h3>
              <ul className="space-y-3">
                {legalLinks.map(link => (
                  <li key={link.href}>
                    <Link 
                      href={link.href} 
                      className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors inline-flex items-center group"
                    >
                      <span className="group-hover:translate-x-1 transition-transform duration-200">
                        {link.label}
                      </span>
                    </Link>
                  </li>
                ))}
                <li>
                  <Link 
                    href="/contact" 
                    className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors inline-flex items-center group"
                  >
                    <span className="group-hover:translate-x-1 transition-transform duration-200">
                      Support Center
                    </span>
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-200 dark:border-gray-700 py-6">
          <div className="flex flex-col-reverse md:flex-row justify-between items-center gap-4">
            
            {/* Copyright */}
            <div className="text-sm text-gray-600 dark:text-gray-400 text-center md:text-left">
              © {currentYear} ResumeRank. All rights reserved.
            </div>

            {/* Developer Credit */}
            <div className="flex flex-wrap items-center justify-center text-sm text-gray-600 dark:text-gray-400 gap-1">
              <span>Designed & developed with</span>
              <Heart className="w-4 h-4 text-red-500 fill-current animate-pulse" />
              <span>by</span>
              <Link 
                href="https://toshankanwar.in/" 
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-semibold transition-colors inline-flex items-center group"
              >
                Toshan Kanwar
                <ExternalLink className="w-3.5 h-3.5 ml-1 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
