'use client'
import { useState, useEffect } from 'react'
import { processResumes } from '../../lib/api'
import FileUpload from '../../components/FileUpload'
import MethodSelector from '../../components/MethodSelector'
import ResultDisplay from '../../components/ResultDisplay'
import { 
  Sparkles, 
  Zap, 
  Brain, 
  BarChart3, 
  Cpu, 
  Database,
  ArrowRight,
  CheckCircle,
  Clock,
  Users,
  FileText,
  Award,
  TrendingUp,
  Play,
  Network,
  TreePine,
  Target,
  Globe,
  Layers
} from 'lucide-react'

export default function PredictPage() {
  const [files, setFiles] = useState([])
  const [jobDescription, setJobDescription] = useState('')
  const [position, setPosition] = useState('sde')
  const [methods, setMethods] = useState(['bert', 'cosine']) // Updated default methods
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [currentStep, setCurrentStep] = useState(1)
  const [processingStage, setProcessingStage] = useState('')
  const [animationCounter, setAnimationCounter] = useState(0)

  // Animation counter for floating elements
  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationCounter(prev => prev + 1)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  // Enhanced processing stages with algorithm-specific messages
  useEffect(() => {
    if (loading) {
      const getStagesForMethods = (selectedMethods) => {
        let stages = ['Parsing resumes...', 'Extracting text content...']
        
        if (selectedMethods.includes('bert')) {
          stages.push('Loading BERT model...', 'Running BERT analysis...')
        }
        if (selectedMethods.includes('distilbert')) {
          stages.push('Loading DistilBERT model...', 'Processing with DistilBERT...')
        }
        if (selectedMethods.includes('sbert')) {
          stages.push('Loading S-BERT model...', 'Computing sentence embeddings...')
        }
        if (selectedMethods.includes('xlm')) {
          stages.push('Loading XLM model...', 'Processing multilingual content...')
        }
        if (selectedMethods.includes('xgboost')) {
          stages.push('Training XGBoost classifier...', 'Running ensemble predictions...')
        }
        if (selectedMethods.includes('random_forest')) {
          stages.push('Building Random Forest...', 'Computing feature importance...')
        }
        if (selectedMethods.includes('svm')) {
          stages.push('Training SVM classifier...', 'Applying kernel methods...')
        }
        if (selectedMethods.includes('neural_network')) {
          stages.push('Initializing neural network...', 'Training deep learning model...')
        }
        if (selectedMethods.includes('cosine')) {
          stages.push('Computing TF-IDF vectors...', 'Calculating cosine similarities...')
        }
        if (selectedMethods.includes('jaccard')) {
          stages.push('Extracting skill sets...', 'Computing Jaccard similarities...')
        }
        if (selectedMethods.includes('ner')) {
          stages.push('Running named entity recognition...', 'Extracting skills and experience...')
        }
        
        stages.push('Combining algorithm results...', 'Generating final rankings...', 'Finalizing analysis...')
        return stages
      }
      
      const stages = getStagesForMethods(methods)
      let stageIndex = 0
      setProcessingStage(stages[0])
      
      const stageInterval = setInterval(() => {
        stageIndex = (stageIndex + 1) % stages.length
        setProcessingStage(stages[stageIndex])
      }, Math.max(800, 4000 / stages.length)) // Adjust timing based on number of stages
      
      return () => clearInterval(stageInterval)
    }
  }, [loading, methods])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!files.length || !jobDescription.trim()) {
      alert('Please upload resumes and enter job description')
      return
    }

    if (methods.length === 0) {
      alert('Please select at least one algorithm')
      return
    }

    setLoading(true)
    setCurrentStep(4)
    
    try {
      const data = await processResumes({ files, jobDescription, position, methods })
      setResults(data)
      setCurrentStep(5)
    } catch (e) {
      alert('Processing failed: ' + e.message)
      setCurrentStep(1)
    } finally {
      setLoading(false)
    }
  }

  const positions = [
    { value: 'sde', label: 'Software Development Engineer', icon: '💻' },
    { value: 'swe', label: 'Software Engineer', icon: '⚙️' },
    { value: 'ml_engineer', label: 'ML Engineer', icon: '🤖' },
    { value: 'data_scientist', label: 'Data Scientist', icon: '📊' },
    { value: 'devops', label: 'DevOps Engineer', icon: '🔧' },
    { value: 'frontend', label: 'Frontend Developer', icon: '🎨' },
    { value: 'backend', label: 'Backend Developer', icon: '🗄️' },
    { value: 'fullstack', label: 'Full Stack Developer', icon: '🚀' },
    { value: 'product_manager', label: 'Product Manager', icon: '📱' },
    { value: 'designer', label: 'UI/UX Designer', icon: '🎭' },
    { value: 'general', label: 'General', icon: '📋' }
  ]

  const steps = [
    { number: 1, title: 'Upload Resumes', desc: 'Select multiple PDF/DOCX files', icon: FileText, active: currentStep >= 1 },
    { number: 2, title: 'Job Details', desc: 'Add description & position', icon: Users, active: currentStep >= 2 },
    { number: 3, title: 'Select Methods', desc: 'Choose AI algorithms', icon: Brain, active: currentStep >= 3 },
    { number: 4, title: 'Processing', desc: 'AI analysis in progress', icon: Zap, active: currentStep >= 4 },
    { number: 5, title: 'Results', desc: 'Ranked candidates ready', icon: Award, active: currentStep >= 5 }
  ]

  // Algorithm icons for dynamic display
  const algorithmIcons = {
    bert: Brain,
    distilbert: Zap,
    sbert: Network,
    xlm: Globe,
    xgboost: TreePine,
    random_forest: Database,
    svm: Target,
    neural_network: Layers,
    cosine: BarChart3,
    jaccard: Cpu,
    ner: Cpu
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-primary-300/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-300/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-green-300/10 rounded-full blur-3xl animate-bounce-light"></div>
      </div>

      <div className="container py-12 relative z-10">
        
        {/* Hero Section */}
        <div className="text-center mb-12 animate-fade-in">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-primary-100 to-purple-100 dark:from-primary-900/30 dark:to-purple-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-6">
            <Sparkles className="w-4 h-4 mr-2 animate-pulse" />
            Advanced Multi-Algorithm Resume Analysis
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary-600 via-purple-600 to-primary-800 bg-clip-text text-transparent">
            Rank Your Candidates
          </h1>
          
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed">
            Upload resumes, define the role, and let our comprehensive AI suite rank candidates using 
            <span className="font-semibold text-primary-600"> Deep Learning</span>,
            <span className="font-semibold text-green-600"> Traditional ML</span>,
            <span className="font-semibold text-purple-600"> NLP Methods</span>, and
            <span className="font-semibold text-orange-600"> Similarity Analysis</span>
          </p>
        </div>

        {/* Progress Steps */}
        <div className="mb-12">
          <div className="flex justify-center items-center space-x-4 md:space-x-8 mb-8">
            {steps.map((step, index) => {
              const Icon = step.icon
              return (
                <div key={index} className="flex items-center">
                  <div className={`relative flex flex-col items-center ${index !== steps.length - 1 ? 'mr-4 md:mr-8' : ''}`}>
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm transition-all duration-500 ${
                      step.active 
                        ? 'bg-gradient-to-r from-primary-500 to-purple-600 text-white shadow-lg animate-pulse' 
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
                    }`}>
                      {currentStep === step.number && loading ? (
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      ) : (
                        <Icon className="w-5 h-5" />
                      )}
                    </div>
                    <div className="text-center mt-2 hidden md:block">
                      <div className={`text-sm font-medium ${step.active ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500'}`}>
                        {step.title}
                      </div>
                      <div className="text-xs text-gray-400">{step.desc}</div>
                    </div>
                  </div>
                  {index < steps.length - 1 && (
                    <div className={`hidden md:block w-16 h-0.5 transition-all duration-500 ${
                      currentStep > step.number ? 'bg-gradient-to-r from-primary-500 to-purple-600' : 'bg-gray-200 dark:bg-gray-700'
                    }`}></div>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Main Form */}
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="space-y-8">
            
            {/* File Upload Section */}
            <div className="card animate-slide-up">
              <div className="flex items-center mb-6">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center mr-4">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white">Upload Resumes</h3>
                  <p className="text-gray-600 dark:text-gray-400">Select multiple PDF or DOCX files to analyze</p>
                </div>
                {files.length > 0 && (
                  <div className="ml-auto flex items-center text-sm text-primary-600 dark:text-primary-400">
                    <CheckCircle className="w-4 h-4 mr-1" />
                    {files.length} file{files.length !== 1 ? 's' : ''} ready
                  </div>
                )}
              </div>
              <FileUpload 
                files={files} 
                setFiles={setFiles} 
                onFilesChange={() => setCurrentStep(Math.max(currentStep, 1))}
              />
            </div>

            {/* Job Description Section */}
            <div className="card animate-slide-up" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-center mb-6">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center mr-4">
                  <Users className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white">Job Description & Position</h3>
                  <p className="text-gray-600 dark:text-gray-400">Provide detailed job requirements and select position type</p>
                </div>
                {jobDescription.trim() && (
                  <div className="ml-auto flex items-center text-sm text-primary-600 dark:text-primary-400">
                    <CheckCircle className="w-4 h-4 mr-1" />
                    Description added
                  </div>
                )}
              </div>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    Job Description *
                  </label>
                  <textarea
                    className="input-field h-48 resize-none"
                    value={jobDescription}
                    onChange={(e) => {
                      setJobDescription(e.target.value)
                      if (e.target.value.trim()) setCurrentStep(Math.max(currentStep, 2))
                    }}
                    placeholder="Paste the complete job description here...

Example:
We are looking for a Senior Software Engineer with 3+ years of experience in React, Node.js, and cloud technologies. The ideal candidate should have strong problem-solving skills and experience with agile development..."
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    Position Type *
                  </label>
                  <div className="grid grid-cols-1 gap-2 max-h-48 overflow-y-auto custom-scrollbar">
                    {positions.map((pos) => (
                      <label key={pos.value} className="cursor-pointer">
                        <input
                          type="radio"
                          name="position"
                          value={pos.value}
                          checked={position === pos.value}
                          onChange={(e) => setPosition(e.target.value)}
                          className="sr-only"
                        />
                        <div className={`flex items-center p-3 rounded-lg border transition-all duration-300 ${
                          position === pos.value
                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-sm'
                            : 'border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600'
                        }`}>
                          <span className="text-xl mr-3">{pos.icon}</span>
                          <span className={`font-medium ${
                            position === pos.value 
                              ? 'text-primary-700 dark:text-primary-300' 
                              : 'text-gray-700 dark:text-gray-300'
                          }`}>
                            {pos.label}
                          </span>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Method Selection */}
            <div className="card animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-center mb-6">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-purple-500 to-violet-500 flex items-center justify-center mr-4">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white">AI Algorithm Selection</h3>
                  <p className="text-gray-600 dark:text-gray-400">Choose which algorithms to use for comprehensive analysis</p>
                </div>
                {methods.length > 0 && (
                  <div className="ml-auto flex items-center text-sm text-primary-600 dark:text-primary-400">
                    <div className="flex -space-x-1 mr-2">
                      {methods.slice(0, 3).map((methodId, index) => {
                        const Icon = algorithmIcons[methodId] || Brain
                        return (
                          <div key={index} className="w-6 h-6 rounded-full bg-primary-500 flex items-center justify-center border-2 border-white">
                            <Icon className="w-3 h-3 text-white" />
                          </div>
                        )
                      })}
                      {methods.length > 3 && (
                        <div className="w-6 h-6 rounded-full bg-gray-500 flex items-center justify-center text-xs text-white border-2 border-white">
                          +{methods.length - 3}
                        </div>
                      )}
                    </div>
                    {methods.length} selected
                  </div>
                )}
              </div>
              <MethodSelector 
                selectedMethods={methods} 
                setSelectedMethods={(newMethods) => {
                  setMethods(newMethods)
                  if (newMethods.length > 0) setCurrentStep(Math.max(currentStep, 3))
                }} 
              />
            </div>

            {/* Submit Button */}
            <div className="text-center animate-slide-up" style={{ animationDelay: '0.3s' }}>
              <button
                type="submit"
                disabled={loading || !files.length || !jobDescription.trim() || methods.length === 0}
                className="group relative inline-flex items-center justify-center px-12 py-4 text-lg font-semibold text-white bg-gradient-to-r from-primary-600 via-purple-600 to-primary-700 rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-primary-700 via-purple-700 to-primary-800 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                
                {loading ? (
                  <>
                    <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin mr-3"></div>
                    <span className="relative z-10">Processing with {methods.length} Algorithm{methods.length !== 1 ? 's' : ''}...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-6 h-6 mr-3 group-hover:animate-pulse relative z-10" />
                    <span className="relative z-10">Start AI Analysis</span>
                    <ArrowRight className="w-5 h-5 ml-3 group-hover:translate-x-1 transition-transform relative z-10" />
                  </>
                )}
              </button>
              
              {loading && (
                <div className="mt-4 p-4 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl border border-primary-200 dark:border-primary-800">
                  <div className="flex items-center justify-center text-primary-700 dark:text-primary-300 font-medium">
                    <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce mr-2"></div>
                    <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce mr-2" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce mr-4" style={{ animationDelay: '0.2s' }}></div>
                    <span className="animate-pulse">{processingStage}</span>
                  </div>
                  
                  {/* Algorithm Progress Indicators */}
                  <div className="flex justify-center mt-3 space-x-2">
                    {methods.map((methodId, index) => {
                      const Icon = algorithmIcons[methodId] || Brain
                      return (
                        <div 
                          key={methodId}
                          className="w-8 h-8 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center animate-pulse"
                          style={{ animationDelay: `${index * 0.2}s` }}
                        >
                          <Icon className="w-4 h-4 text-primary-600 dark:text-primary-400" />
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}
            </div>
          </form>

          {/* Results Section */}
          {results && !loading && (
            <div className="mt-12 animate-fade-in">
              <div className="text-center mb-8">
                <div className="inline-flex items-center px-6 py-3 rounded-full bg-gradient-to-r from-green-100 to-emerald-100 dark:from-green-900/30 dark:to-emerald-900/30 text-green-700 dark:text-green-300 font-medium mb-4">
                  <CheckCircle className="w-5 h-5 mr-2" />
                  Multi-Algorithm Analysis Complete!
                </div>
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                  Resume Rankings
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  Results from {methods.length} AI algorithm{methods.length !== 1 ? 's' : ''}, sorted by combined confidence score
                </p>
              </div>
              <ResultDisplay results={results} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
