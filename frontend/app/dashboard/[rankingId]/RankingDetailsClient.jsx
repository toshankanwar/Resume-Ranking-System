'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { auth, db } from '../../../lib/firebase'
import { collection, doc, getDoc, getDocs } from 'firebase/firestore'
import {
  ArrowLeft,
  Trophy,
  Medal,
  Award,
  Star,
  FileText,
  Calendar,
  Cpu,
  Download,
  Eye,
  TrendingUp,
} from 'lucide-react'

export const runtime = 'edge'
export default function RankingDetailsClient({ rankingId }) {
  const router = useRouter()
  const [user, setUser] = useState(null)
  const [ranking, setRanking] = useState(null)
  const [details, setDetails] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsub = auth.onAuthStateChanged(async u => {
      setUser(u)
      if (u && u.emailVerified) {
        await fetchDetails(u.uid)
      } else {
        setLoading(false)
      }
    })
    return () => unsub()
  }, [rankingId])

  const fetchDetails = async userId => {
    try {
      setLoading(true)

      // Fetch ranking summary
      const rankingRef = doc(db, 'users', userId, 'rankings', rankingId)
      const rankingSnap = await getDoc(rankingRef)

      if (!rankingSnap.exists()) {
        router.push('/dashboard')
        return
      }

      setRanking({
        id: rankingSnap.id,
        ...rankingSnap.data(),
        createdAt: rankingSnap.data().createdAt?.toDate() || new Date(),
      })

      // Fetch all details
      const detailsRef = collection(db, 'users', userId, 'rankings', rankingId, 'details')
      const detailsSnap = await getDocs(detailsRef)

      const detailsData = detailsSnap.docs
        .map(doc => ({
          id: doc.id,
          ...doc.data(),
        }))
        .sort((a, b) => (a.rank || 0) - (b.rank || 0))

      setDetails(detailsData)
    } catch (error) {
      console.error('Error fetching details:', error)
    } finally {
      setLoading(false)
    }
  }

  const getRankIcon = rank => {
    switch (rank) {
      case 1:
        return <Trophy className="w-5 h-5 text-yellow-500" />
      case 2:
        return <Medal className="w-5 h-5 text-gray-400" />
      case 3:
        return <Award className="w-5 h-5 text-orange-500" />
      default:
        return <Star className="w-5 h-5 text-gray-400" />
    }
  }

  const getScoreColor = score => {
    if (score >= 0.8) return 'text-green-600 dark:text-green-400'
    if (score >= 0.6) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  const getScoreBgClass = score => {
    if (score >= 0.8) return 'bg-green-100 dark:bg-green-900/30'
    if (score >= 0.6) return 'bg-yellow-100 dark:bg-yellow-900/30'
    return 'bg-red-100 dark:bg-red-900/30'
  }

  const exportToCSV = () => {
    if (details.length === 0) return

    const algorithms = Object.keys(details[0].scores || {})
    const headers = ['Rank', 'Filename', ...algorithms.map(a => `${a.toUpperCase()} (%)`), 'Final Score (%)']

    const csvData = details.map(detail => [
      detail.rank,
      detail.filename,
      ...algorithms.map(alg => detail.scores?.[alg] ? (detail.scores[alg] * 100).toFixed(1) : 'N/A'),
      detail.finalScore ? (detail.finalScore * 100).toFixed(1) : 'N/A',
    ])

    const csvContent = [headers, ...csvData]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `ranking_${rankingId}_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  const formatDate = date => {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading ranking details...</p>
        </div>
      </div>
    )
  }

  if (!user || !user.emailVerified || !ranking) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">No Data Found</h2>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-xl font-medium transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    )
  }

  const allAlgorithms = details.length > 0 ? Object.keys(details[0].scores || {}).sort() : []

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-100/50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-primary-300/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-300/10 rounded-full blur-3xl animate-float"></div>
      </div>

      <div className="container py-12 relative z-10">
        {/* Back Button */}
        <button
          onClick={() => router.push('/dashboard')}
          className="flex items-center text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-6 transition-colors"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Dashboard
        </button>

        {/* Header */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 border border-gray-200 dark:border-gray-700 shadow-lg mb-8">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                {ranking.position?.replace('_', ' ').toUpperCase() || 'General'} Position Analysis
              </h1>
              <div className="flex items-center text-gray-600 dark:text-gray-400">
                <Calendar className="w-5 h-5 mr-2" />
                {formatDate(ranking.createdAt)}
              </div>
            </div>
            <button
              onClick={exportToCSV}
              className="flex items-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl text-sm font-medium transition-colors"
            >
              <Download className="w-4 h-4 mr-2" />
              Export CSV
            </button>
          </div>

          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
              <FileText className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900 dark:text-white">{ranking.filesCount || 0}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Resumes Analyzed</div>
            </div>

            <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-xl">
              <Cpu className="w-8 h-8 text-purple-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900 dark:text-white">{ranking.methods?.length || 0}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">AI Methods</div>
            </div>

            <div className="text-center p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-xl">
              <Trophy className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
              <div className="text-sm font-bold text-gray-900 dark:text-white truncate" title={ranking.topCandidate}>
                {ranking.topCandidate || 'N/A'}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Top Candidate</div>
            </div>

            <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-xl">
              <TrendingUp className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {details.length > 0
                  ? ((details.reduce((acc, d) => acc + (d.finalScore || 0), 0) / details.length) * 100).toFixed(1) + '%'
                  : 'N/A'}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Avg Score</div>
            </div>
          </div>

          {ranking.methods && ranking.methods.length > 0 && (
            <div className="mt-6">
              <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">Algorithms Used:</h3>
              <div className="flex flex-wrap gap-2">
                {ranking.methods.map((method, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-800 dark:text-primary-200 rounded-full text-sm font-medium"
                  >
                    {method.replace('_', ' ').toUpperCase()}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Results Table */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-lg">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Detailed Results</h2>
            <p className="text-gray-600 dark:text-gray-400">Complete ranking breakdown for all candidates</p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-900/50">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Rank
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Filename
                  </th>
                  {allAlgorithms.map(alg => (
                    <th
                      key={alg}
                      className="px-6 py-4 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                    >
                      {alg.replace('_', ' ')}
                    </th>
                  ))}
                  <th className="px-6 py-4 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Final Score
                  </th>
                  <th className="px-6 py-4 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Skills
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {details.map((detail, index) => (
                  <tr
                    key={detail.id}
                    className={`hover:bg-gray-50 dark:hover:bg-gray-800/50 ${
                      detail.rank <= 3 ? 'bg-yellow-50 dark:bg-yellow-900/10' : ''
                    }`}
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div
                          className={`w-10 h-10 rounded-full flex items-center justify-center mr-3 ${
                            detail.rank <= 3
                              ? 'bg-gradient-to-r from-yellow-400 to-orange-500'
                              : 'bg-gray-200 dark:bg-gray-700'
                          } shadow-sm`}
                        >
                          <span className="font-bold text-white">#{detail.rank}</span>
                        </div>
                        {getRankIcon(detail.rank)}
                      </div>
                    </td>

                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900 dark:text-white max-w-xs truncate" title={detail.filename}>
                        {detail.filename}
                      </div>
                      {detail.fileInfo && (
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {detail.fileInfo.word_count || 0} words
                        </div>
                      )}
                    </td>

                    {allAlgorithms.map(alg => (
                      <td key={alg} className="px-6 py-4 text-center">
                        {detail.scores?.[alg] !== undefined ? (
                          <div
                            className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${getScoreBgClass(
                              detail.scores[alg]
                            )}`}
                          >
                            <span className={getScoreColor(detail.scores[alg])}>
                              {(detail.scores[alg] * 100).toFixed(1)}%
                            </span>
                          </div>
                        ) : (
                          <span className="text-gray-400 dark:text-gray-500 text-xs">N/A</span>
                        )}
                      </td>
                    ))}

                    <td className="px-6 py-4 text-center">
                      {detail.finalScore ? (
                        <div
                          className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-bold ${getScoreBgClass(
                            detail.finalScore
                          )}`}
                        >
                          <span className={getScoreColor(detail.finalScore)}>
                            {(detail.finalScore * 100).toFixed(1)}%
                          </span>
                        </div>
                      ) : (
                        <span className="text-gray-400 dark:text-gray-500 text-sm">N/A</span>
                      )}
                    </td>

                    <td className="px-6 py-4 text-center">
                      <span className="inline-flex items-center px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 rounded-full text-xs font-medium">
                        {detail.extractedSkills?.length || 0}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
