'use client'
import { useState } from 'react'
import Link from 'next/link'
import { useForm } from 'react-hook-form'
import { 
  Mail, 
  MessageSquare, 
  Send, 
  Github, 
  Globe, 
  MapPin, 
  Clock, 
  CheckCircle,
  ArrowRight,
  Phone,
  Linkedin,
  Twitter,
  Heart,
  Sparkles,
  Zap,
  Code,
  Users,
  Star,
  Award,
  TrendingUp,
  Calendar,
  Shield
} from 'lucide-react'

export default function ContactPage() {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [submitMessage, setSubmitMessage] = useState('')

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm()

  const onSubmit = async (data) => {
    setIsSubmitting(true)
    
    try {
      const formData = new FormData()
      
      // Web3Forms configuration
      formData.append('access_key', process.env.NEXT_PUBLIC_WEB3FORMS_ACCESS_KEY || 'b8a13edd-5d10-492a-992f-40dc5acd7849')
      formData.append('name', data.name)
      formData.append('email', data.email)
      formData.append('subject', data.subject || 'Contact from ResumeRank AI')
      formData.append('message', data.message)
      formData.append('from_name', 'ResumeRank AI Contact Form')
      formData.append('replyto', data.email)
      
      const response = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        body: formData
      })

      const result = await response.json()

      if (result.success) {
        setIsSubmitted(true)
        setSubmitMessage('Thank you! Your message has been sent successfully.')
        reset()
        
        // Reset success state after 5 seconds
        setTimeout(() => {
          setIsSubmitted(false)
          setSubmitMessage('')
        }, 5000)
      } else {
        throw new Error(result.message || 'Something went wrong')
      }
    } catch (error) {
      setSubmitMessage('Failed to send message. Please try again.')
      console.error('Form submission error:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const contactInfo = [
    {
      icon: Mail,
      title: 'Email',
      content: 'contact@toshankanwar.website',
      link: 'mailto:contact@toshankanwar.website',
      color: 'text-blue-600 dark:text-blue-400',
      bg: 'bg-blue-100 dark:bg-blue-900/30'
    },
    {
      icon: Github,
      title: 'GitHub',
      content: 'github.com/toshankanwar',
      link: 'https://github.com/toshankanwar',
      color: 'text-gray-700 dark:text-gray-300',
      bg: 'bg-gray-100 dark:bg-gray-800'
    },
    {
      icon: Globe,
      title: 'Website',
      content: 'toshankanwar.website',
      link: 'https://toshankanwar.website',
      color: 'text-green-600 dark:text-green-400',
      bg: 'bg-green-100 dark:bg-green-900/30'
    },
    {
      icon: Linkedin,
      title: 'LinkedIn',
      content: 'Connect professionally',
      link: 'https://www.linkedin.com/in/toshan-kanwar-4683a1349/',
      color: 'text-blue-700 dark:text-blue-300',
      bg: 'bg-blue-100 dark:bg-blue-900/30'
    }
  ]

  const features = [
    {
      icon: Zap,
      title: 'AI-Powered Analysis',
      description: 'Advanced machine learning algorithms for accurate resume ranking'
    },
    {
      icon: Code,
      title: 'Open Source',
      description: 'Built with modern technologies and available on GitHub'
    },
    {
      icon: Users,
      title: 'Scalable Solution',
      description: 'Handle thousands of resumes efficiently with parallel processing'
    },
    {
      icon: Shield,
      title: 'Privacy First',
      description: 'Your data is secure and processed with enterprise-grade security'
    }
  ]

  const stats = [
    { icon: Star, value: '90%', label: 'Accuracy Rate' },
    { icon: Users, value: '10+', label: 'Resumes Processed' },
    { icon: TrendingUp, value: '5x', label: 'Faster Screening' },
    { icon: Award, value: '10+', label: 'AI Algorithms' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-primary-300/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-300/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-gradient-to-r from-pink-300/10 to-yellow-300/10 rounded-full blur-3xl animate-pulse"></div>
      </div>

      <div className="container relative z-10 py-8">
        
        {/* Hero Section */}
        <div className="text-center mb-12 animate-fade-in">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-primary-100 to-purple-100 dark:from-primary-900/30 dark:to-purple-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-6">
            <MessageSquare className="w-4 h-4 mr-2" />
            Get In Touch
          </div>
          
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-primary-600 via-purple-600 to-primary-800 bg-clip-text text-transparent">
            Let's Connect
          </h1>
          
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto leading-relaxed">
            Have questions about our AI resume ranking system? Ready to revolutionize your hiring process? 
            Let's discuss how we can help you find the perfect candidates faster.
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-3 gap-8 mb-12">
            
            {/* Contact Form - Takes 2 columns */}
            <div className="lg:col-span-2">
              <div className="card animate-slide-in-left h-full">
                <div className="flex items-center mb-6">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-primary-500 to-purple-600 flex items-center justify-center mr-4">
                    <Send className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Send a Message</h2>
                    <p className="text-gray-600 dark:text-gray-400">We typically respond within 24 hours</p>
                  </div>
                </div>

                {isSubmitted ? (
                  <div className="text-center py-8 animate-scale-in">
                    <div className="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mx-auto mb-4">
                      <CheckCircle className="w-8 h-8 text-green-600 dark:text-green-400" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Message Sent!</h3>
                    <p className="text-gray-600 dark:text-gray-400">{submitMessage}</p>
                  </div>
                ) : (
                  <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                    {/* Anti-spam honeypot */}
                    <input 
                      type="checkbox" 
                      name="botcheck" 
                      className="hidden" 
                      style={{ display: 'none' }}
                      {...register('botcheck')}
                    />

                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                          Full Name *
                        </label>
                        <input
                          type="text"
                          className={`input-field ${errors.name ? 'border-red-500 focus:border-red-500' : ''}`}
                          placeholder="Your full name"
                          {...register('name', { 
                            required: 'Full name is required',
                            maxLength: { value: 80, message: 'Name is too long' }
                          })}
                        />
                        {errors.name && (
                          <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                        )}
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                          Email Address *
                        </label>
                        <input
                          type="email"
                          className={`input-field ${errors.email ? 'border-red-500 focus:border-red-500' : ''}`}
                          placeholder="your.email@example.com"
                          {...register('email', { 
                            required: 'Email is required',
                            pattern: {
                              value: /^\S+@\S+$/i,
                              message: 'Please enter a valid email'
                            }
                          })}
                        />
                        {errors.email && (
                          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
                        )}
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Subject
                      </label>
                      <input
                        type="text"
                        className="input-field"
                        placeholder="What's this about?"
                        {...register('subject')}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Message *
                      </label>
                      <textarea
                        rows={5}
                        className={`input-field resize-none ${errors.message ? 'border-red-500 focus:border-red-500' : ''}`}
                        placeholder="Tell us about your project, questions, or how we can help you optimize your hiring process..."
                        {...register('message', { 
                          required: 'Message is required',
                          minLength: { value: 10, message: 'Message should be at least 10 characters' }
                        })}
                      />
                      {errors.message && (
                        <p className="mt-1 text-sm text-red-600">{errors.message.message}</p>
                      )}
                    </div>

                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="group w-full inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-primary-600 via-purple-600 to-primary-700 rounded-2xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                    >
                      {isSubmitting ? (
                        <>
                          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-3"></div>
                          Sending Message...
                        </>
                      ) : (
                        <>
                          <Send className="w-5 h-5 mr-3 group-hover:animate-pulse" />
                          Send Message
                          <ArrowRight className="w-5 h-5 ml-3 group-hover:translate-x-1 transition-transform" />
                        </>
                      )}
                    </button>

                    {submitMessage && !isSubmitted && (
                      <div className="text-center text-red-600 dark:text-red-400">
                        {submitMessage}
                      </div>
                    )}
                  </form>
                )}
              </div>
            </div>

            {/* Contact Info Sidebar */}
            <div className="space-y-6 animate-slide-in-right">
              
              {/* Contact Details */}
              <div className="card">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Contact Information</h3>
                <div className="space-y-3">
                  {contactInfo.map((info, index) => {
                    const Icon = info.icon
                    return (
                      <Link
                        key={index}
                        href={info.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-all duration-300 group"
                      >
                        <div className={`w-10 h-10 rounded-lg ${info.bg} flex items-center justify-center mr-3 group-hover:scale-110 transition-transform`}>
                          <Icon className={`w-5 h-5 ${info.color}`} />
                        </div>
                        <div className="flex-1">
                          <div className="font-medium text-gray-900 dark:text-white text-sm">
                            {info.title}
                          </div>
                          <div className="text-xs text-gray-600 dark:text-gray-400 truncate">
                            {info.content}
                          </div>
                        </div>
                      </Link>
                    )
                  })}
                </div>
              </div>

              {/* Response Times */}
              <div className="card">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Response Times</h3>
                <div className="space-y-3">
                  <div className="flex items-center text-sm">
                    <Clock className="w-4 h-4 text-green-600 mr-3 flex-shrink-0" />
                    <span className="text-gray-600 dark:text-gray-400">General inquiries: <strong className="text-gray-900 dark:text-white">24 hours</strong></span>
                  </div>
                  <div className="flex items-center text-sm">
                    <Clock className="w-4 h-4 text-blue-600 mr-3 flex-shrink-0" />
                    <span className="text-gray-600 dark:text-gray-400">Technical support: <strong className="text-gray-900 dark:text-white">48 hours</strong></span>
                  </div>
                  <div className="flex items-center text-sm">
                    <Calendar className="w-4 h-4 text-purple-600 mr-3 flex-shrink-0" />
                    <span className="text-gray-600 dark:text-gray-400">Partnerships: <strong className="text-gray-900 dark:text-white">72 hours</strong></span>
                  </div>
                </div>
              </div>

              {/* Developer Info */}
              <div className="card bg-gradient-to-br from-primary-50 to-purple-50 dark:from-primary-900/20 dark:to-purple-900/20 border-primary-200 dark:border-primary-700">
                <div className="flex items-center mb-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-primary-600 to-purple-600 flex items-center justify-center mr-3">
                    <Heart className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-primary-900 dark:text-primary-100">Meet the Developer</h3>
                    <p className="text-primary-700 dark:text-primary-300 text-sm">Toshan Kanwar</p>
                  </div>
                </div>
                <p className="text-primary-800 dark:text-primary-200 text-sm leading-relaxed mb-3">
                  Computer Science student passionate about AI, machine learning, and making hiring processes more efficient.
                </p>
                <Link
                  href="https://toshankanwar.website"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-primary-700 dark:text-primary-300 hover:text-primary-600 dark:hover:text-primary-200 font-medium text-sm group"
                >
                  <Globe className="w-4 h-4 mr-2" />
                  Visit Portfolio
                  <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                </Link>
              </div>
            </div>
          </div>

          {/* Stats Section */}
          <div className="grid md:grid-cols-4 gap-6 mb-12 animate-fade-in-up">
            {stats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <div key={index} className="card text-center hover:shadow-lg transition-shadow">
                  <Icon className="w-8 h-8 mx-auto mb-3 text-primary-600 dark:text-primary-400" />
                  <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">{stat.value}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">{stat.label}</div>
                </div>
              )
            })}
          </div>

          {/* Features Section */}
          <div className="mb-12">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Why Choose ResumeRank AI?</h2>
              <p className="text-gray-600 dark:text-gray-400">Discover what makes our solution stand out</p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 animate-fade-in-up">
              {features.map((feature, index) => {
                const Icon = feature.icon
                return (
                  <div key={index} className="card text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                    <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-r from-primary-100 to-purple-100 dark:from-primary-900/30 dark:to-purple-900/30 flex items-center justify-center">
                      <Icon className="w-6 h-6 text-primary-600 dark:text-primary-400" />
                    </div>
                    <h3 className="font-bold text-gray-900 dark:text-white mb-2">{feature.title}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">{feature.description}</p>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="card bg-gradient-to-r from-primary-600 to-purple-600 text-white text-center animate-fade-in-up">
            <div className="max-w-3xl mx-auto">
              <h2 className="text-2xl font-bold mb-3">Ready to Get Started?</h2>
              <p className="text-primary-100 mb-6">Try our AI-powered resume ranking system now and see the difference</p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  href="/predict"
                  className="inline-flex items-center px-6 py-3 bg-white text-primary-600 rounded-xl font-semibold hover:bg-gray-100 transition-colors"
                >
                  <Sparkles className="w-5 h-5 mr-2" />
                  Try Demo
                </Link>
                <Link
                  href="/about"
                  className="inline-flex items-center px-6 py-3 border-2 border-white text-white rounded-xl font-semibold hover:bg-white hover:text-primary-600 transition-colors"
                >
                  <MessageSquare className="w-5 h-5 mr-2" />
                  Learn More
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
