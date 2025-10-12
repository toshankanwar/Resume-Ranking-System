'use client'
import { Brain, BarChart3, Cpu, Database, Zap, Network, TreePine, Target, Globe, Layers } from 'lucide-react'

export default function MethodSelector({ selectedMethods, setSelectedMethods }) {
  const methodCategories = [
    {
      title: "Deep Learning & Transformers",
      methods: [
        { 
          id: 'bert', 
          name: 'BERT Semantic Analysis', 
          desc: 'Bidirectional transformer for deep contextual understanding',
          icon: Brain,
          color: 'from-blue-500 to-cyan-500',
          features: ['Context-aware', 'Bidirectional', 'State-of-the-art'],
          speed: 'Medium'
        },
        { 
          id: 'distilbert', 
          name: 'DistilBERT', 
          desc: 'Lighter, faster version of BERT with 97% of performance',
          icon: Zap,
          color: 'from-cyan-400 to-blue-500',
          features: ['Fast', 'Efficient', 'High accuracy'],
          speed: 'Fast'
        },
        { 
          id: 'sbert', 
          name: 'S-BERT (Sentence-BERT)', 
          desc: 'Optimized for sentence-level embeddings and similarity',
          icon: Network,
          color: 'from-indigo-500 to-purple-500',
          features: ['Sentence-level', 'Similarity optimized', 'Embeddings'],
          speed: 'Fast'
        }
      ]
    },
    {
      title: "Traditional ML Algorithms",
      methods: [
        { 
          id: 'xgboost', 
          name: 'XGBoost Classifier', 
          desc: 'Gradient boosting with ensemble learning for classification',
          icon: TreePine,
          color: 'from-green-500 to-emerald-500',
          features: ['Ensemble', 'High performance', 'Feature importance'],
          speed: 'Fast'
        },
        { 
          id: 'random_forest', 
          name: 'Random Forest', 
          desc: 'Ensemble method combining multiple decision trees',
          icon: Database,
          color: 'from-emerald-500 to-green-600',
          features: ['Robust', 'Interpretable', 'Feature ranking'],
          speed: 'Very Fast'
        },
        { 
          id: 'svm', 
          name: 'Support Vector Machine', 
          desc: 'SVM with RBF kernel for high-dimensional text classification',
          icon: Target,
          color: 'from-orange-500 to-red-500',
          features: ['Powerful', 'Kernel methods', 'Margin optimization'],
          speed: 'Medium'
        },
        { 
          id: 'neural_network', 
          name: 'Neural Network (MLP)', 
          desc: 'Multi-layer perceptron for complex pattern recognition',
          icon: Layers,
          color: 'from-red-500 to-pink-500',
          features: ['Deep learning', 'Pattern recognition', 'Non-linear'],
          speed: 'Medium'
        }
      ]
    },
    {
      title: "Similarity & NLP Methods",
      methods: [
        { 
          id: 'cosine', 
          name: 'TF-IDF Cosine Similarity', 
          desc: 'Statistical keyword matching with mathematical precision',
          icon: BarChart3,
          color: 'from-yellow-500 to-orange-500',
          features: ['Fast processing', 'Keyword matching', 'Statistical'],
          speed: 'Very Fast'
        },
        { 
          id: 'jaccard', 
          name: 'Jaccard Similarity', 
          desc: 'Skill-focused similarity for competency matching',
          icon: Cpu,
          color: 'from-teal-500 to-cyan-500',
          features: ['Skill matching', 'Set-based', 'Competency focused'],
          speed: 'Very Fast'
        },
        { 
          id: 'ner', 
          name: 'Named Entity Recognition', 
          desc: 'Extract skills, experience, and qualifications intelligently',
          icon: Cpu,
          color: 'from-purple-500 to-violet-500',
          features: ['Skill extraction', 'Experience parsing', 'Entity recognition'],
          speed: 'Fast'
        }
      ]
    }
  ]

  const toggleMethod = (methodId) => {
    setSelectedMethods(prev => 
      prev.includes(methodId) 
        ? prev.filter(m => m !== methodId)
        : [...prev, methodId]
    )
  }

  const selectCategory = (categoryMethods) => {
    const categoryIds = categoryMethods.map(m => m.id)
    const allSelected = categoryIds.every(id => selectedMethods.includes(id))
    
    if (allSelected) {
      // Deselect all in category
      setSelectedMethods(prev => prev.filter(id => !categoryIds.includes(id)))
    } else {
      // Select all in category
      setSelectedMethods(prev => [...new Set([...prev, ...categoryIds])])
    }
  }

  const getSpeedColor = (speed) => {
    switch(speed) {
      case 'Very Fast': return 'text-green-600 dark:text-green-400'
      case 'Fast': return 'text-blue-600 dark:text-blue-400'
      case 'Medium': return 'text-yellow-600 dark:text-yellow-400'
      default: return 'text-gray-600 dark:text-gray-400'
    }
  }

  return (
    <div className="space-y-8">
      {methodCategories.map((category, categoryIndex) => (
        <div key={categoryIndex} className="space-y-4">
          {/* Category Header */}
          <div className="flex items-center justify-between">
            <h4 className="text-lg font-bold text-gray-900 dark:text-white">
              {category.title}
            </h4>
            <button
              onClick={() => selectCategory(category.methods)}
              className="text-sm px-3 py-1 rounded-lg bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors"
            >
              {category.methods.every(m => selectedMethods.includes(m.id)) ? 'Deselect All' : 'Select All'}
            </button>
          </div>

          {/* Methods Grid */}
          <div className="grid md:grid-cols-2 gap-4">
            {category.methods.map((method, index) => {
              const Icon = method.icon
              const isSelected = selectedMethods.includes(method.id)
              
              return (
                <div 
                  key={method.id}
                  className="animate-scale-in"
                  style={{ animationDelay: `${(categoryIndex * 4 + index) * 0.1}s` }}
                >
                  <label className="cursor-pointer group block h-full">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => toggleMethod(method.id)}
                      className="sr-only"
                    />
                    <div className={`relative p-6 rounded-2xl border-2 transition-all duration-300 h-full ${
                      isSelected
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-lg'
                        : 'border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-md hover:bg-gray-50/50 dark:hover:bg-gray-800/30'
                    }`}>
                      
                      {/* Selection Indicator */}
                      <div className={`absolute top-4 right-4 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all duration-300 ${
                        isSelected
                          ? 'border-primary-500 bg-primary-500'
                          : 'border-gray-300 dark:border-gray-600 group-hover:border-primary-400'
                      }`}>
                        {isSelected && (
                          <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        )}
                      </div>

                      {/* Icon */}
                      <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${method.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                        <Icon className="w-6 h-6 text-white" />
                      </div>

                      {/* Content */}
                      <div className="space-y-4">
                        <div>
                          <h3 className={`font-bold text-lg mb-2 transition-colors ${
                            isSelected 
                              ? 'text-primary-700 dark:text-primary-300' 
                              : 'text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400'
                          }`}>
                            {method.name}
                          </h3>
                          <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed mb-3">
                            {method.desc}
                          </p>
                        </div>

                        {/* Speed Indicator */}
                        <div className="text-right">
                          <span className="text-gray-500 dark:text-gray-400 text-xs">Speed: </span>
                          <span className={`font-semibold text-xs ${getSpeedColor(method.speed)}`}>
                            {method.speed}
                          </span>
                        </div>
                        
                        {/* Features */}
                        <div className="flex flex-wrap gap-1">
                          {method.features.map((feature, idx) => (
                            <span
                              key={idx}
                              className={`text-xs px-2 py-1 rounded-full transition-colors ${
                                isSelected
                                  ? 'bg-primary-100 dark:bg-primary-800 text-primary-700 dark:text-primary-300'
                                  : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'
                              }`}
                            >
                              {feature}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </label>
                </div>
              )
            })}
          </div>
        </div>
      ))}

      {/* Selection Summary */}
      {selectedMethods.length > 0 && (
        <div className="p-6 bg-primary-50 dark:bg-primary-900/20 rounded-xl border border-primary-200 dark:border-primary-800 animate-fade-in">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="text-lg font-semibold text-primary-700 dark:text-primary-300 mb-2">
                Selected Algorithms ({selectedMethods.length})
              </div>
              <div className="text-sm text-primary-600 dark:text-primary-400 mb-4">
                Your resumes will be analyzed using multiple AI algorithms for comprehensive evaluation
              </div>
              
              {/* Selected Methods List */}
              <div className="flex flex-wrap gap-2">
                {selectedMethods.map(methodId => {
                  const method = methodCategories
                    .flatMap(cat => cat.methods)
                    .find(m => m.id === methodId)
                  return method ? (
                    <span 
                      key={methodId}
                      className="inline-flex items-center px-3 py-1 rounded-full text-xs bg-primary-100 dark:bg-primary-800 text-primary-700 dark:text-primary-300"
                    >
                      {method.name}
                    </span>
                  ) : null
                })}
              </div>
            </div>

            {/* Quick Recommendations */}
            <div className="ml-6 text-right">
              <div className="text-xs text-primary-600 dark:text-primary-400 mb-2">Quick Select:</div>
              <div className="space-y-1">
                <button
                  onClick={() => setSelectedMethods(['bert', 'cosine', 'ner'])}
                  className="block text-xs px-2 py-1 rounded bg-primary-200 dark:bg-primary-800 text-primary-800 dark:text-primary-200 hover:bg-primary-300 dark:hover:bg-primary-700 transition-colors"
                >
                  🚀 Recommended
                </button>
                <button
                  onClick={() => setSelectedMethods(['distilbert', 'jaccard'])}
                  className="block text-xs px-2 py-1 rounded bg-green-200 dark:bg-green-800 text-green-800 dark:text-green-200 hover:bg-green-300 dark:hover:bg-green-700 transition-colors"
                >
                  ⚡ Fast
                </button>
                <button
                  onClick={() => setSelectedMethods(['bert', 'sbert', 'xgboost', 'ner'])}
                  className="block text-xs px-2 py-1 rounded bg-purple-200 dark:bg-purple-800 text-purple-800 dark:text-purple-200 hover:bg-purple-300 dark:hover:bg-purple-700 transition-colors"
                >
                  🎯 Comprehensive
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
