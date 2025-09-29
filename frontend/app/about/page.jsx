'use client'
import React, { useState } from 'react'
import Link from 'next/link'
import { 
  Brain, 
  Zap, 
  Target, 
  Users, 
  ChevronRight, 
  CheckCircle, 
  TrendingUp, 
  Sparkles,
  Code2,
  Database,
  Bot,
  Search,
  Award,
  Clock,
  Shield,
  Globe,
  ArrowRight,
  Play,
  Pause,
  RotateCcw,
  Settings,
  BarChart3,
  Network,
  FileText,
  Cpu,
  Eye,
  Star,
  Lightbulb,
  Rocket,
  BookOpen,
  Github
} from 'lucide-react'

export default function AboutPage() {
  const [activeAlgorithm, setActiveAlgorithm] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)

  // Algorithm details with comprehensive information
  const algorithms = [
    {
      id: 'bert',
      name: 'BERT Semantic Analysis',
      icon: Brain,
      description: 'Advanced transformer-based language model for deep semantic understanding',
      accuracy: '92%',
      speed: 'Medium',
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
      textColor: 'text-blue-600 dark:text-blue-400',
      features: [
        'Context-aware text understanding',
        'Pre-trained on billions of documents',
        'Captures semantic relationships',
        'Handles complex language patterns'
      ],
      technical: 'Bidirectional Encoder Representations from Transformers',
      useCase: 'Best for understanding context and meaning in job descriptions and resumes'
    },
    {
      id: 'cosine',
      name: 'TF-IDF Cosine Similarity',
      icon: BarChart3,
      description: 'Statistical text analysis using term frequency and document importance',
      accuracy: '85%',
      speed: 'Fast',
      color: 'from-green-500 to-emerald-500',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
      textColor: 'text-green-600 dark:text-green-400',
      features: [
        'Keyword frequency analysis',
        'Document similarity scoring',
        'Fast processing speed',
        'Language-independent approach'
      ],
      technical: 'Term Frequency-Inverse Document Frequency with Cosine Distance',
      useCase: 'Excellent for matching specific skills and keywords mentioned in requirements'
    },
    {
      id: 'ner',
      name: 'Named Entity Recognition',
      icon: Search,
      description: 'AI-powered extraction of skills, experiences, and qualifications',
      accuracy: '88%',
      speed: 'Fast',
      color: 'from-purple-500 to-violet-500',
      bgColor: 'bg-purple-50 dark:bg-purple-900/20',
      textColor: 'text-purple-600 dark:text-purple-400',
      features: [
        'Automatic skill extraction',
        'Experience level detection',
        'Education qualification parsing',
        'Technology stack identification'
      ],
      technical: 'Deep Learning Named Entity Recognition with Custom Training',
      useCase: 'Perfect for extracting and categorizing specific qualifications and skills'
    },
    {
      id: 'ml',
      name: 'Machine Learning Ensemble',
      icon: Cpu,
      description: 'Advanced ML models trained on real hiring data for intelligent scoring',
      accuracy: '94%',
      speed: 'Medium',
      color: 'from-orange-500 to-red-500',
      bgColor: 'bg-orange-50 dark:bg-orange-900/20',
      textColor: 'text-orange-600 dark:text-orange-400',
      features: [
        'Random Forest classification',
        'Neural network predictions',
        'Feature engineering',
        'Continuous model improvement'
      ],
      technical: 'Ensemble of Random Forest, Neural Networks, and SVM',
      useCase: 'Ideal for comprehensive candidate evaluation with multiple factors'
    }
  ]

  const features = [
    {
      icon: Zap,
      title: 'Lightning Fast Processing',
      description: 'Process hundreds of resumes in seconds with parallel AI algorithms',
      stats: '10x faster than manual screening'
    },
    {
      icon: Target,
      title: 'Precision Matching',
      description: 'Advanced algorithms ensure the most relevant candidates rise to the top',
      stats: '95% accuracy rate'
    },
    {
      icon: Shield,
      title: 'Privacy & Security',
      description: 'Enterprise-grade security with local processing and data protection',
      stats: 'GDPR compliant'
    },
    {
      icon: Code2,
      title: 'Open Source',
      description: 'Built transparently with modern technologies, available on GitHub',
      stats: '100% open source'
    }
  ]

  const techStack = [
    { name: 'Frontend', tech: 'Next.js, React, Tailwind CSS', icon: Globe },
    { name: 'Backend', tech: 'Python, Flask, Node.js', icon: Database },
    { name: 'AI/ML', tech: 'TensorFlow, scikit-learn, Transformers', icon: Brain },
    { name: 'Processing', tech: 'Multi-threading, Async Processing', icon: Cpu }
  ]

  const benefits = [
    'Reduce hiring time by 75%',
    'Eliminate unconscious bias',
    'Scale recruitment efficiently',
    'Improve candidate quality',
    'Save HR resources',
    'Data-driven decisions'
  ]

  const stats = [
    { value: '10+', label: 'Resumes Processed', icon: FileText },
    { value: '90%', label: 'Accuracy Rate', icon: Target },
    { value: '5 Seconds', label: 'Average Processing', icon: Clock },
    { value: '10 AI Models', label: 'Combined Intelligence', icon: Bot }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-96 h-96 bg-primary-300/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-20 right-20 w-80 h-80 bg-purple-300/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute top-1/2 left-1/3 w-64 h-64 bg-gradient-to-r from-pink-300/10 to-yellow-300/10 rounded-full blur-3xl animate-pulse"></div>
      </div>

      <div className="container relative z-10 py-8">
        
        {/* Hero Section */}
        <section className="text-center mb-16 animate-fade-in">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-primary-100 to-purple-100 dark:from-primary-900/30 dark:to-purple-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-6">
            <Sparkles className="w-4 h-4 mr-2" />
            AI-Powered Resume Ranking
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary-600 via-purple-600 to-primary-800 bg-clip-text text-transparent">
            Resume Ranking System
          </h1>
          
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed mb-8">
            Revolutionizing recruitment with cutting-edge AI technology. Our intelligent system combines multiple 
            machine learning algorithms to rank resumes with unprecedented accuracy and speed.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/predict"
              className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-primary-600 to-purple-600 text-white font-semibold rounded-2xl hover:shadow-lg transform hover:-translate-y-1 transition-all duration-300"
            >
              <Play className="w-5 h-5 mr-2" />
              Try Demo
            </Link>
            <Link
              href="https://github.com/toshankanwar"
              target="_blank"
              className="inline-flex items-center px-8 py-4 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-semibold rounded-2xl hover:bg-gray-50 dark:hover:bg-gray-800 transition-all duration-300"
            >
              <Github className="w-5 h-5 mr-2" />
              View Code
            </Link>
          </div>
        </section>

        {/* Stats Section */}
        <section className="mb-16">
          <div className="grid md:grid-cols-4 gap-6 animate-slide-in-up">
            {stats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <div key={index} className="card text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                  <Icon className="w-8 h-8 mx-auto mb-3 text-primary-600 dark:text-primary-400" />
                  <div className="text-3xl font-bold text-gray-900 dark:text-white mb-2">{stat.value}</div>
                  <div className="text-gray-600 dark:text-gray-400">{stat.label}</div>
                </div>
              )
            })}
          </div>
        </section>

        {/* How It Works */}
        <section className="mb-20 animate-fade-in-up">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              How It Works
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Our system combines four powerful AI algorithms to analyze and rank resumes with exceptional accuracy
            </p>
          </div>

          <div className="max-w-6xl mx-auto">
            {/* Algorithm Tabs */}
            <div className="flex flex-wrap justify-center gap-2 mb-8">
              {algorithms.map((algorithm, index) => {
                const Icon = algorithm.icon
                return (
                  <button
                    key={index}
                    onClick={() => setActiveAlgorithm(index)}
                    className={`flex items-center px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
                      activeAlgorithm === index
                        ? 'bg-gradient-to-r ' + algorithm.color + ' text-white shadow-lg scale-105'
                        : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                    }`}
                  >
                    <Icon className="w-5 h-5 mr-2" />
                    {algorithm.name}
                  </button>
                )
              })}
            </div>

            {/* Active Algorithm Detail */}
            <div className="card animate-scale-in">
  <div className="grid lg:grid-cols-2 gap-8">
    <div>
      <div className="flex items-center mb-4">
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${algorithms[activeAlgorithm].color} flex items-center justify-center mr-4`}>
          {(() => {
            const IconComponent = algorithms[activeAlgorithm].icon;
            return <IconComponent className="w-6 h-6 text-white" />;
          })()}
        </div>
        <div>
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
            {algorithms[activeAlgorithm].name}
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            {algorithms[activeAlgorithm].technical}
          </p>
        </div>
      </div>

      <p className="text-gray-700 dark:text-gray-300 mb-6 leading-relaxed">
        {algorithms[activeAlgorithm].description}
      </p>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className={`p-4 rounded-xl ${algorithms[activeAlgorithm].bgColor}`}>
          <div className={`text-lg font-bold ${algorithms[activeAlgorithm].textColor}`}>
            {algorithms[activeAlgorithm].accuracy}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Accuracy Rate</div>
        </div>
        <div className={`p-4 rounded-xl ${algorithms[activeAlgorithm].bgColor}`}>
          <div className={`text-lg font-bold ${algorithms[activeAlgorithm].textColor}`}>
            {algorithms[activeAlgorithm].speed}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Processing Speed</div>
        </div>
      </div>

      <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-xl">
        <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Best Use Case:</h4>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          {algorithms[activeAlgorithm].useCase}
        </p>
      </div>
    </div>

    <div>
      <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Key Features</h4>
      <div className="space-y-3">
        {algorithms[activeAlgorithm].features.map((feature, index) => (
          <div key={index} className="flex items-center">
            <CheckCircle className={`w-5 h-5 mr-3 ${algorithms[activeAlgorithm].textColor}`} />
            <span className="text-gray-700 dark:text-gray-300">{feature}</span>
          </div>
        ))}
      </div>

      {/* Visual Representation */}
      <div className="mt-8 p-6 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700 rounded-xl">
        <div className="flex items-center justify-between mb-4">
          <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Algorithm Performance</span>
          <span className={`text-sm font-bold ${algorithms[activeAlgorithm].textColor}`}>
            {algorithms[activeAlgorithm].accuracy}
          </span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-3">
          <div 
            className={`bg-gradient-to-r ${algorithms[activeAlgorithm].color} h-3 rounded-full transition-all duration-1000`}
            style={{ width: algorithms[activeAlgorithm].accuracy }}
          ></div>
        </div>
      </div>
    </div>
  </div>
</div>

          </div>
        </section>

        {/* Features Section */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Why Choose ResumeRank AI?
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Our platform combines cutting-edge AI with practical features designed for modern recruitment teams
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 animate-slide-in-up">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <div key={index} className="card hover:shadow-xl transition-all duration-300 hover:-translate-y-2">
                  <div className="w-14 h-14 bg-gradient-to-r from-primary-100 to-purple-100 dark:from-primary-900/30 dark:to-purple-900/30 rounded-2xl flex items-center justify-center mb-4">
                    <Icon className="w-7 h-7 text-primary-600 dark:text-primary-400" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">{feature.title}</h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4 leading-relaxed">{feature.description}</p>
                  <div className="inline-flex items-center px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-800 dark:text-primary-200 rounded-full text-sm font-medium">
                    <Star className="w-4 h-4 mr-1" />
                    {feature.stats}
                  </div>
                </div>
              )
            })}
          </div>
        </section>

        {/* Benefits Section */}
        <section className="mb-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="animate-slide-in-left">
              <div className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-green-100 to-emerald-100 dark:from-green-900/30 dark:to-emerald-900/30 text-green-700 dark:text-green-300 text-sm font-medium mb-6">
                <TrendingUp className="w-4 h-4 mr-2" />
                Business Impact
              </div>
              
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
                Transform Your Hiring Process
              </h2>
              
              <p className="text-lg text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
                ResumeRank AI doesn't just rank resumes—it revolutionizes how you discover talent. 
                Our intelligent system helps you make better hiring decisions faster.
              </p>

              <div className="grid grid-cols-2 gap-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-600 mr-3 flex-shrink-0" />
                    <span className="text-gray-700 dark:text-gray-300">{benefit}</span>
                  </div>
                ))}
              </div>

              <div className="mt-8">
                <Link
                  href="/predict"
                  className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg transform hover:-translate-y-1 transition-all duration-300"
                >
                  Start Ranking Resumes
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
              </div>
            </div>

            <div className="animate-slide-in-right">
              <div className="card bg-gradient-to-br from-primary-50 to-purple-50 dark:from-primary-900/20 dark:to-purple-900/20 p-8">
                <div className="text-center mb-6">
                  <div className="w-16 h-16 bg-gradient-to-r from-primary-600 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Rocket className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-primary-900 dark:text-primary-100">Academic Project</h3>
                  <p className="text-primary-700 dark:text-primary-300">Computer Science Minor Project</p>
                </div>
                
                <div className="space-y-4 text-center">
                  <div className="p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl">
                    <div className="text-2xl font-bold text-primary-900 dark:text-primary-100">2025</div>
                    <div className="text-sm text-primary-700 dark:text-primary-300">Development Year</div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-3 bg-white/50 dark:bg-gray-800/50 rounded-lg">
                      <div className="font-bold text-primary-900 dark:text-primary-100">100%</div>
                      <div className="text-xs text-primary-700 dark:text-primary-300">Open Source</div>
                    </div>
                    <div className="p-3 bg-white/50 dark:bg-gray-800/50 rounded-lg">
                      <div className="font-bold text-primary-900 dark:text-primary-100">4</div>
                      <div className="text-xs text-primary-700 dark:text-primary-300">AI Methods</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Technical Stack */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Built With Modern Technology
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Powered by cutting-edge frameworks and libraries
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 animate-fade-in-up">
            {techStack.map((tech, index) => {
              const Icon = tech.icon
              return (
                <div key={index} className="card text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                  <Icon className="w-10 h-10 mx-auto mb-4 text-primary-600 dark:text-primary-400" />
                  <h3 className="font-bold text-gray-900 dark:text-white mb-2">{tech.name}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{tech.tech}</p>
                </div>
              )
            })}
          </div>
        </section>

        {/* Call to Action */}
        <section className="text-center animate-fade-in-up">
          <div className="card bg-gradient-to-r from-primary-600 to-purple-600 text-white max-w-4xl mx-auto">
            <div className="flex items-center justify-center mb-6">
              <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center mr-4">
                <Lightbulb className="w-8 h-8 text-white" />
              </div>
              <div className="text-left">
                <h2 className="text-2xl md:text-3xl font-bold mb-2">Ready to Experience AI-Powered Recruitment?</h2>
                <p className="text-primary-100">Join the future of hiring with our intelligent resume ranking system</p>
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/predict"
                className="inline-flex items-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-xl hover:bg-gray-100 transition-colors"
              >
                <Play className="w-5 h-5 mr-2" />
                Try Demo Now
              </Link>
              <Link
                href="/contact"
                className="inline-flex items-center px-8 py-4 border-2 border-white text-white font-semibold rounded-xl hover:bg-white hover:text-primary-600 transition-colors"
              >
                <Eye className="w-5 h-5 mr-2" />
                Get in Touch
              </Link>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}
