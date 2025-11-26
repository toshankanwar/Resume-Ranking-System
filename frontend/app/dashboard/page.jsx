'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { auth, db } from '@/lib/firebase'
import { collection, query, orderBy, getDocs } from 'firebase/firestore'
import {
  Calendar,
  FileText,
  TrendingUp,
  Award,
  ChevronRight,
  Filter,
  Clock,
  Briefcase,
  Cpu,
  Users,
  ArrowUpDown,
} from 'lucide-react'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState(null)
  const [rankings, setRankings] = useState([])
  const [loading, setLoading] = useState(true)
  const [sortOrder, setSortOrder] = useState('latest') // 'latest' or 'oldest'

  useEffect(() => {
    const unsub = auth.onAuthStateChanged(async u => {
      setUser(u)
      if (u && u.emailVerified) {
        await fetchRankings(u.uid)
      } else {
        setLoading(false)
      }
    })
    return () => unsub()
  }, [])

  const fetchRankings = async (userId) => {
    try {
      setLoading(true)
      const rankingsRef = collection(db, 'users', userId, 'rankings')
      const q = query(rankingsRef, orderBy('createdAt', 'desc'))
      const snapshot = await getDocs(q)

      const rankingsData = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data(),
        createdAt: doc.data().createdAt?.toDate() || new Date(),
      }))

      setRankings(rankingsData)
    } catch (error) {
      console.error('Error fetching rankings:', error)
    } finally {
      setLoading(false)
    }
  }

  const sortedRankings = [...rankings].sort((a, b) => {
    if (sortOrder === 'latest') {
      return b.createdAt - a.createdAt
    } else {
      return a.createdAt - b.createdAt
    }
  })

  const formatDate = date => {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date)
  }

  const getMethodIcon = method => {
    const icons = {
      bert: '🧠',
      cosine: '📊',
      sbert: '🔍',
      distilbert: '⚡',
      xgboost: '🌲',
      random_forest: '🌳',
      svm: '🎯',
      neural_network: '🔗',
      jaccard: '💡',
      ner: '📝',
      xlm: '🌍',
    }
    return icons[method] || '🤖'
  }

  const getPositionIcon = position => {
    const icons = {
      sde: '💻',
      swe: '⚙️',
      ml_engineer: '🤖',
      data_scientist: '📊',
      devops: '🔧',
      frontend: '🎨',
      backend: '🗄️',
      fullstack: '🚀',
      product_manager: '📱',
      designer: '🎭',
      general: '📋',
    }
    return icons[position] || '💼'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading your rankings...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Please Log In</h2>
          <p className="text-gray-600 dark:text-gray-400">You need to be logged in to view your rankings.</p>
        </div>
      </div>
    )
  }

  if (!user.emailVerified) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <Award className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Email Not Verified</h2>
          <p className="text-gray-600 dark:text-gray-400">Please verify your email to access rankings.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-primary-300/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-300/10 rounded-full blur-3xl animate-float"></div>
      </div>

      <div className="container py-12 relative z-10">
        {/* Header */}
        <div className="mb-12 animate-fade-in">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-primary-600 via-purple-600 to-primary-800 bg-clip-text text-transparent">
            Your Rankings Dashboard
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            View and manage all your resume ranking analyses
          </p>
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-8 h-8 text-primary-600" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">{rankings.length}</span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Total Analyses</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <FileText className="w-8 h-8 text-green-600" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {rankings.reduce((acc, r) => acc + (r.filesCount || 0), 0)}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Resumes Processed</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <Cpu className="w-8 h-8 text-purple-600" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {rankings.reduce((acc, r) => acc + (r.methods?.length || 0), 0)}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">AI Methods Used</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <Award className="w-8 h-8 text-yellow-600" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {rankings.filter(r => r.topCandidate).length}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Top Candidates</p>
          </div>
        </div>

        {/* Sort Controls */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
            <Filter className="w-6 h-6 mr-2" />
            All Rankings
          </h2>
          <div className="flex items-center bg-white dark:bg-gray-800 rounded-xl p-1 border border-gray-200 dark:border-gray-700">
            <button
              onClick={() => setSortOrder('latest')}
              className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                sortOrder === 'latest'
                  ? 'bg-primary-600 text-white shadow-sm'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
            >
              <ArrowUpDown className="w-4 h-4 mr-2" />
              Latest First
            </button>
            <button
              onClick={() => setSortOrder('oldest')}
              className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                sortOrder === 'oldest'
                  ? 'bg-primary-600 text-white shadow-sm'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
            >
              <ArrowUpDown className="w-4 h-4 mr-2" />
              Oldest First
            </button>
          </div>
        </div>

        {/* Rankings List */}
        {sortedRankings.length === 0 ? (
          <div className="text-center py-20">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">No Rankings Yet</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Start by analyzing some resumes to see them here.
            </p>
            <button
              onClick={() => router.push('/predict')}
              className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-xl font-medium transition-colors"
            >
              Analyze Resumes
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {sortedRankings.map((ranking, index) => (
              <div
                key={ranking.id}
                onClick={() => router.push(`/dashboard/${ranking.id}`)}
                className="card hover:shadow-xl cursor-pointer transform hover:-translate-y-1 transition-all duration-300 animate-slide-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center mb-3">
                      <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-primary-500 to-purple-600 flex items-center justify-center mr-4">
                        <FileText className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center">
                          {getPositionIcon(ranking.position)} {ranking.position?.replace('_', ' ').toUpperCase() || 'General'} Analysis
                        </h3>
                        <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                          <Clock className="w-4 h-4 mr-1" />
                          {formatDate(ranking.createdAt)}
                        </div>
                      </div>
                    </div>

                    <div className="grid md:grid-cols-3 gap-4 mb-4">
                      <div className="flex items-center text-sm">
                        <FileText className="w-5 h-5 text-blue-600 mr-2" />
                        <div>
                          <div className="font-semibold text-gray-900 dark:text-white">{ranking.filesCount || 0}</div>
                          <div className="text-gray-600 dark:text-gray-400">Resumes</div>
                        </div>
                      </div>

                      <div className="flex items-center text-sm">
                        <Cpu className="w-5 h-5 text-purple-600 mr-2" />
                        <div>
                          <div className="font-semibold text-gray-900 dark:text-white">{ranking.methods?.length || 0}</div>
                          <div className="text-gray-600 dark:text-gray-400">AI Methods</div>
                        </div>
                      </div>

                      <div className="flex items-center text-sm">
                        <Award className="w-5 h-5 text-yellow-600 mr-2" />
                        <div>
                          <div className="font-semibold text-gray-900 dark:text-white truncate max-w-[150px]" title={ranking.topCandidate}>
                            {ranking.topCandidate || 'N/A'}
                          </div>
                          <div className="text-gray-600 dark:text-gray-400">Top Candidate</div>
                        </div>
                      </div>
                    </div>

                    {ranking.methods && ranking.methods.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {ranking.methods.map((method, idx) => (
                          <span
                            key={idx}
                            className="inline-flex items-center px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-800 dark:text-primary-200 rounded-full text-xs font-medium"
                          >
                            {getMethodIcon(method)} {method.replace('_', ' ').toUpperCase()}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>

                  <ChevronRight className="w-6 h-6 text-gray-400 ml-4 flex-shrink-0" />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
