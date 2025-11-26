import { notFound } from 'next/navigation'
import { collection, doc, getDoc, getDocs } from 'firebase/firestore'
import { db } from '@/lib/firebase'
import RankingDetailsClient from './RankingDetailsClient'

// Enable static generation
export const dynamic = 'force-static'
export const dynamicParams = true

async function getRankingDetails(rankingId, userId) {
  try {
    // Fetch ranking summary
    const rankingRef = doc(db, 'users', userId, 'rankings', rankingId)
    const rankingSnap = await getDoc(rankingRef)

    if (!rankingSnap.exists()) {
      return null
    }

    // Fetch all details
    const detailsRef = collection(db, 'users', userId, 'rankings', rankingId, 'details')
    const detailsSnap = await getDocs(detailsRef)

    const details = detailsSnap.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
    }))

    return {
      ranking: {
        id: rankingSnap.id,
        ...rankingSnap.data(),
      },
      details: details.sort((a, b) => (a.rank || 0) - (b.rank || 0)),
    }
  } catch (error) {
    console.error('Error fetching ranking details:', error)
    return null
  }
}

export default async function RankingDetailsPage({ params }) {
  const { rankingId } = await params

  // Note: In production, you'd get userId from auth on client side
  // For now, this is a placeholder - actual implementation needs client-side auth
  
  return <RankingDetailsClient rankingId={rankingId} />
}
