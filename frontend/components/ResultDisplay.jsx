'use client'
import { useState } from 'react'
import { Trophy, Medal, Award, Star, TrendingUp, Users, Clock, CheckCircle, Table, Grid3X3, Download, Eye } from 'lucide-react'

export default function ResultDisplay({ results }) {
  const [viewMode, setViewMode] = useState('cards') // 'cards' or 'table'
  
  if (!results?.results) return null

  const getRankIcon = (rank) => {
    switch(rank) {
      case 1: return <Trophy className="w-5 h-5 text-yellow-500" />
      case 2: return <Medal className="w-5 h-5 text-gray-400" />
      case 3: return <Award className="w-5 h-5 text-orange-500" />
      default: return <Star className="w-5 h-5 text-gray-400" />
    }
  }

  const getScoreColor = (score) => {
    if (score >= 0.8) return 'text-green-600 dark:text-green-400'
    if (score >= 0.6) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  const getScoreBg = (score) => {
    if (score >= 0.8) return 'from-green-500 to-emerald-500'
    if (score >= 0.6) return 'from-yellow-500 to-orange-500'
    return 'from-red-500 to-pink-500'
  }

  const getScoreBgClass = (score) => {
    if (score >= 0.8) return 'bg-green-100 dark:bg-green-900/30'
    if (score >= 0.6) return 'bg-yellow-100 dark:bg-yellow-900/30'
    return 'bg-red-100 dark:bg-red-900/30'
  }

  // Get all unique algorithms from results
  const getAlgorithms = () => {
    const algorithms = new Set()
    results.results.forEach(result => {
      if (result.scores) {
        Object.keys(result.scores).forEach(alg => algorithms.add(alg))
      }
    })
    return Array.from(algorithms).sort()
  }

  const algorithms = getAlgorithms()

  // Export to CSV function
  const exportToCSV = () => {
    const headers = ['Rank', 'Filename', ...algorithms.map(alg => `${alg.toUpperCase()} (%)`), 'Final Score (%)', 'Skills Count']
    
    const csvData = results.results.map(result => [
      result.rank,
      result.filename,
      ...algorithms.map(alg => result.scores?.[alg] ? (result.scores[alg] * 100).toFixed(1) : 'N/A'),
      result.final_score ? (result.final_score * 100).toFixed(1) : 'N/A',
      result.extracted_skills?.length || 0
    ])

    const csvContent = [headers, ...csvData]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `resume_ranking_results_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="grid md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 text-center">
          <Users className="w-8 h-8 mx-auto mb-3 text-primary-600" />
          <div className="text-2xl font-bold text-gray-900 dark:text-white">{results.summary?.total_resumes_uploaded || 0}</div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Total Resumes</div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 text-center">
          <CheckCircle className="w-8 h-8 mx-auto mb-3 text-green-600" />
          <div className="text-2xl font-bold text-gray-900 dark:text-white">{results.summary?.successfully_processed || 0}</div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Processed</div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 text-center">
          <TrendingUp className="w-8 h-8 mx-auto mb-3 text-purple-600" />
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {results.results?.length > 0 ? 
              ((results.results.reduce((acc, r) => acc + (r.final_score || 0), 0) / results.results.length) * 100).toFixed(1) + '%' 
              : 'N/A'
            }
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Avg Score</div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 text-center">
          <Clock className="w-8 h-8 mx-auto mb-3 text-blue-600" />
          <div className="text-2xl font-bold text-gray-900 dark:text-white">{results.summary?.algorithms_used?.length || 0}</div>
          <div className="text-sm text-gray-600 dark:text-gray-400">AI Methods</div>
        </div>
      </div>

      {/* View Toggle and Export */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div className="flex items-center bg-gray-100 dark:bg-gray-800 rounded-xl p-1">
          <button
            onClick={() => setViewMode('cards')}
            className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              viewMode === 'cards'
                ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            <Grid3X3 className="w-4 h-4 mr-2" />
            Card View
          </button>
          <button
            onClick={() => setViewMode('table')}
            className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              viewMode === 'table'
                ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            <Table className="w-4 h-4 mr-2" />
            Table View
          </button>
        </div>

        <button
          onClick={exportToCSV}
          className="flex items-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl text-sm font-medium transition-colors"
        >
          <Download className="w-4 h-4 mr-2" />
          Export CSV
        </button>
      </div>

      {/* Table View */}
      {viewMode === 'table' && (
        <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-900/50">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Rank
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Resume File
                  </th>
                  {algorithms.map(algorithm => (
                    <th key={algorithm} className="px-6 py-4 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      {algorithm.replace('_', ' ')}
                    </th>
                  ))}
                  <th className="px-6 py-4 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Final Score
                  </th>
                  <th className="px-6 py-4 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Skills
                  </th>
                  <th className="px-6 py-4 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {results.results.map((result, index) => (
                  <tr key={index} className={`hover:bg-gray-50 dark:hover:bg-gray-800/50 ${
                    result.rank <= 3 ? 'bg-yellow-50 dark:bg-yellow-900/10' : ''
                  }`}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                          result.rank <= 3 ? 'bg-gradient-to-r from-yellow-400 to-orange-500' : 'bg-gray-200 dark:bg-gray-700'
                        } shadow-sm`}>
                          <span className="font-bold text-white text-sm">#{result.rank}</span>
                        </div>
                        {getRankIcon(result.rank)}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900 dark:text-white max-w-xs truncate" title={result.filename}>
                        {result.filename}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {result.file_info?.word_count || 0} words
                      </div>
                    </td>
                    {algorithms.map(algorithm => (
                      <td key={algorithm} className="px-6 py-4 text-center">
                        {result.scores?.[algorithm] ? (
                          <div className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                            getScoreBgClass(result.scores[algorithm])
                          }`}>
                            <span className={getScoreColor(result.scores[algorithm])}>
                              {(result.scores[algorithm] * 100).toFixed(1)}%
                            </span>
                          </div>
                        ) : (
                          <span className="text-gray-400 dark:text-gray-500 text-xs">N/A</span>
                        )}
                      </td>
                    ))}
                    <td className="px-6 py-4 text-center">
                      {result.final_score ? (
                        <div className={`inline-flex items-center px-3 py-2 rounded-full text-sm font-bold ${
                          getScoreBgClass(result.final_score)
                        }`}>
                          <span className={getScoreColor(result.final_score)}>
                            {(result.final_score * 100).toFixed(1)}%
                          </span>
                        </div>
                      ) : (
                        <span className="text-gray-400 dark:text-gray-500 text-sm">N/A</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className="inline-flex items-center px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 rounded-full text-xs font-medium">
                        {result.extracted_skills?.length || 0}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <button
                        onClick={() => {
                          // Toggle to detailed view for this specific resume
                          const element = document.getElementById(`result-${index}`)
                          if (element) {
                            element.scrollIntoView({ behavior: 'smooth' })
                            setViewMode('cards')
                          }
                        }}
                        className="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
                        title="View Details"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Cards View */}
      {viewMode === 'cards' && (
        <div className="space-y-4">
          {results.results.map((result, index) => (
            <div 
              key={index} 
              id={`result-${index}`}
              className="card hover:shadow-xl transition-all duration-300 animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center space-x-4">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                    result.rank <= 3 ? 'bg-gradient-to-r from-yellow-400 to-orange-500' : 'bg-gray-200 dark:bg-gray-700'
                  } shadow-lg`}>
                    <span className="font-bold text-white">#{result.rank}</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white flex items-center">
                      {result.filename}
                      <span className="ml-2">{getRankIcon(result.rank)}</span>
                    </h3>
                    {result.error ? (
                      <p className="text-red-600 dark:text-red-400 text-sm">{result.error}</p>
                    ) : (
                      <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                        <span>{result.extracted_skills?.length || 0} skills identified</span>
                        <span>•</span>
                        <span>{result.file_info?.word_count || 0} words</span>
                      </div>
                    )}
                  </div>
                </div>
                
                {result.final_score && (
                  <div className="text-right">
                    <div className={`text-3xl font-bold ${getScoreColor(result.final_score)}`}>
                      {(result.final_score * 100).toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">Overall Match</div>
                  </div>
                )}
              </div>

              {result.scores && (
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                  {Object.entries(result.scores).map(([method, score]) => (
                    <div key={method} className="text-center p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
                      <div className={`text-lg font-bold ${getScoreColor(score)}`}>
                        {(score * 100).toFixed(1)}%
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 capitalize">
                        {method.replace('_', ' ')}
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-2">
                        <div 
                          className={`bg-gradient-to-r ${getScoreBg(score)} h-2 rounded-full transition-all duration-500`}
                          style={{ width: `${score * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {result.explanation && (
                <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl border-l-4 border-blue-500">
                  <h4 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">Analysis Summary</h4>
                  <p className="text-blue-800 dark:text-blue-200 text-sm leading-relaxed">
                    {result.explanation}
                  </p>
                </div>
              )}

              {result.extracted_skills?.length > 0 && (
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                    Extracted Skills ({result.extracted_skills.length})
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {result.extracted_skills.slice(0, 10).map((skill, i) => (
                      <span
                        key={i}
                        className="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 rounded-full text-sm font-medium"
                      >
                        {skill}
                      </span>
                    ))}
                    {result.extracted_skills.length > 10 && (
                      <span className="px-3 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded-full text-sm">
                        +{result.extracted_skills.length - 10} more
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
