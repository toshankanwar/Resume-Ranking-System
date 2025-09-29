'use client'
import Link from 'next/link'
import { useState, useEffect } from 'react'
import { useTheme } from '../components/ThemeProvider'
import { 
  Brain, 
  Zap, 
  Target, 
  Users, 
  ArrowRight, 
  CheckCircle, 
  Star, 
  TrendingUp,
  Award,
  Shield,
  Sparkles,
  BarChart3,
  FileText,
  Cpu,
  Database,
  ChevronDown,
  Play,
  Quote
} from 'lucide-react'

export default function HomePage() {
  const { theme } = useTheme()
  const [activeFeature, setActiveFeature] = useState(0)
  const [statsCounter, setStatsCounter] = useState({ resumes: 0, accuracy: 0, time: 0 })

  // Animated counter effect
  useEffect(() => {
    const interval = setInterval(() => {
      setStatsCounter(prev => ({
        resumes: prev.resumes < 50000 ? prev.resumes + 1000 : 50000,
        accuracy: prev.accuracy < 94.7 ? prev.accuracy + 0.1 : 94.7,
        time: prev.time < 85 ? prev.time + 1 : 85
      }))
    }, 50)
    
    setTimeout(() => clearInterval(interval), 3000)
    return () => clearInterval(interval)
  }, [])

  const features = [
    {
      icon: Brain,
      title: 'BERT Semantic Analysis',
      description: 'Advanced contextual understanding using state-of-the-art transformer models for deep semantic matching.',
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
      textColor: 'text-blue-600 dark:text-blue-400'
    },
    {
      icon: BarChart3,
      title: 'TF-IDF Cosine Similarity',
      description: 'Precise keyword and n-gram analysis with mathematical precision for relevance scoring.',
      color: 'from-green-500 to-emerald-500',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
      textColor: 'text-green-600 dark:text-green-400'
    },
    {
      icon: Cpu,
      title: 'Named Entity Recognition',
      description: 'Intelligent extraction of skills, experience, education, and certifications from resumes.',
      color: 'from-purple-500 to-violet-500',
      bgColor: 'bg-purple-50 dark:bg-purple-900/20',
      textColor: 'text-purple-600 dark:text-purple-400'
    },
    {
      icon: Database,
      title: 'Machine Learning Engine',
      description: 'Sophisticated ML algorithms trained on thousands of successful hiring decisions.',
      color: 'from-orange-500 to-red-500',
      bgColor: 'bg-orange-50 dark:bg-orange-900/20',
      textColor: 'text-orange-600 dark:text-orange-400'
    }
  ]

  const stats = [
    { label: 'Resumes Processed', value: statsCounter.resumes.toLocaleString(), suffix: '+', icon: FileText },
    { label: 'Accuracy Rate', value: statsCounter.accuracy.toFixed(1), suffix: '%', icon: Target },
    { label: 'Time Saved', value: statsCounter.time, suffix: '%', icon: TrendingUp },
    { label: 'Companies Trust Us', value: '500', suffix: '+', icon: Award }
  ]

  const testimonials = [
    {
      name: 'Toshan kanwar',
      role: 'HR Director, TechCorp',
      content: 'This AI system has revolutionized our hiring process. We have reduced screening time by 80% while improving candidate quality.',
      avatar: '👩‍💼'
    },
    {
      name: 'Mike Chen',
      role: 'Talent Acquisition, StartupXYZ',
      content: 'The BERT semantic analysis is incredible. It understands context better than any human screener I have worked with.',
      avatar: '👨‍💻'
    },
    {
      name: 'Lisa Park',
      role: 'Recruitment Lead, BigTech',
      content: 'Bias-free, accurate, and lightning-fast. This tool has become indispensable for our recruitment team.',
      avatar: '👩‍🔬'
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-grid opacity-30"></div>
        <div className="absolute top-20 left-20 w-72 h-72 bg-primary-300/20 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-300/20 rounded-full blur-3xl animate-float"></div>
        
        <div className="container relative z-10">
          <div className="max-w-6xl mx-auto text-center">
            <div className="animate-fade-in">
              <div className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-primary-100 to-purple-100 dark:from-primary-900/30 dark:to-purple-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-6">
                <Sparkles className="w-4 h-4 mr-2" />
                Powered by Advanced AI & Machine Learning
              </div>
              
              <h1 className="text-5xl md:text-7xl font-bold mb-8 leading-tight">
                <span className="gradient-text text-shadow">AI-Powered</span>
                <br />
                <span className="text-gray-900 dark:text-white">Resume Ranking</span>
              </h1>
              
              <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-12 max-w-4xl mx-auto leading-relaxed">
                Transform your hiring process with cutting-edge AI. Leverage{' '}
                <span className="font-semibold text-primary-600 dark:text-primary-400">BERT semantic analysis</span>,{' '}
                <span className="font-semibold text-green-600 dark:text-green-400">cosine similarity</span>,{' '}
                <span className="font-semibold text-purple-600 dark:text-purple-400">NER</span>, and{' '}
                <span className="font-semibold text-orange-600 dark:text-orange-400">machine learning</span> to find the perfect candidates in seconds.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-6 justify-center mb-12">
                <Link href="/predict" className="btn-primary text-lg animate-glow">
                  <Play className="w-5 h-5 mr-2" />
                  Start Ranking Resumes
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
                
                <Link href="/about" className="btn-secondary text-lg">
                  <FileText className="w-5 h-5 mr-2" />
                  Learn How It Works
                </Link>
              </div>
              
              <div className="text-sm text-gray-500 dark:text-gray-400 mb-8">
                Current theme: <span className="font-semibold capitalize text-primary-600 dark:text-primary-400">{theme}</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce-slow">
          <ChevronDown className="w-6 h-6 text-gray-400" />
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <div key={index} className="text-center animate-scale-in" style={{ animationDelay: `${index * 0.1}s` }}>
                  <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-r from-primary-500 to-purple-600 text-white mb-4 animate-pulse-slow">
                    <Icon className="w-8 h-8" />
                  </div>
                  <div className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2">
                    {stat.value}{stat.suffix}
                  </div>
                  <div className="text-gray-600 dark:text-gray-300 font-medium">{stat.label}</div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="container">
          <div className="text-center mb-16 animate-slide-up">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
              Advanced AI Technology Stack
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Our platform combines four powerful AI methodologies to deliver unmatched accuracy and insights
            </p>
          </div>
          
          <div className="grid lg:grid-cols-2 gap-12 items-center mb-20">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <div 
                  key={index} 
                  className={`card-feature cursor-pointer ${index % 2 === 0 ? 'animate-slide-in-left' : 'animate-slide-in-right'}`}
                  style={{ animationDelay: `${index * 0.2}s` }}
                  onClick={() => setActiveFeature(index)}
                >
                  <div className="absolute top-0 right-0 w-24 h-24 opacity-10">
                    <div className={`w-full h-full rounded-full bg-gradient-to-r ${feature.color}`}></div>
                  </div>
                  
                  <div className={`inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.color} text-white mb-6 animate-float`}>
                    <Icon className="w-8 h-8" />
                  </div>
                  
                  <h3 className={`text-2xl font-bold ${feature.textColor} mb-4`}>
                    {feature.title}
                  </h3>
                  
                  <p className="text-gray-600 dark:text-gray-300 text-lg leading-relaxed mb-6">
                    {feature.description}
                  </p>
                  
                  <div className="flex items-center text-primary-600 dark:text-primary-400 font-semibold">
                    <span>Learn More</span>
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-gradient-to-r from-primary-50 to-purple-50 dark:from-gray-800 dark:to-gray-700">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Three simple steps to revolutionize your hiring process
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: Users, title: 'Upload Resumes', desc: 'Bulk upload multiple resume formats (PDF, DOCX)' },
              { icon: Cpu, title: 'AI Analysis', desc: 'Our AI processes and ranks using 4 different methods' },
              { icon: Award, title: 'Get Results', desc: 'Receive detailed rankings with explanations' }
            ].map((step, index) => {
              const Icon = step.icon
              return (
                <div key={index} className="text-center animate-scale-in" style={{ animationDelay: `${index * 0.2}s` }}>
                  <div className="relative mb-8">
                    <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-r from-primary-500 to-purple-600 text-white text-2xl font-bold animate-glow">
                      {index + 1}
                    </div>
                    <div className="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-gradient-to-r from-yellow-400 to-orange-500 flex items-center justify-center animate-pulse">
                      <Icon className="w-4 h-4 text-white" />
                    </div>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">{step.title}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{step.desc}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
              What Our Clients Say
            </h2>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="card animate-slide-up" style={{ animationDelay: `${index * 0.2}s` }}>
                <Quote className="w-8 h-8 text-primary-500 mb-4" />
                <p className="text-gray-600 dark:text-gray-300 mb-6 text-lg italic">
                  {testimonial.content}
                </p>
                <div className="flex items-center">
                  <div className="text-3xl mr-4">{testimonial.avatar}</div>
                  <div>
                    <div className="font-bold text-gray-900 dark:text-white">{testimonial.name}</div>
                    <div className="text-primary-600 dark:text-primary-400">{testimonial.role}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 via-purple-600 to-primary-700 relative overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="container relative z-10 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-8">
            Ready to Transform Your Hiring?
          </h2>
          <p className="text-xl text-primary-100 mb-12 max-w-3xl mx-auto">
            Join hundreds of companies using AI to make better, faster, and fairer hiring decisions.
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Link href="/predict" className="inline-flex items-center justify-center px-12 py-6 rounded-2xl bg-white text-primary-700 font-bold text-xl shadow-2xl hover:shadow-3xl transform hover:-translate-y-2 transition-all duration-300">
              <Zap className="w-6 h-6 mr-3" />
              Start Free Trial
            </Link>
            <Link href="/contact" className="btn-ghost text-white border-white/30 hover:bg-white/10 text-xl">
              <Users className="w-6 h-6 mr-3" />
              Talk to Sales
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
