'use client';

import { useState, useEffect } from 'react';
import { auth, db } from '@/lib/firebase';
import {
  sendEmailVerification,
  deleteUser,
} from 'firebase/auth';
import { useRouter } from 'next/navigation';
import { doc, deleteDoc } from 'firebase/firestore';

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sendingVerification, setSendingVerification] = useState(false);
  const [deletingAccount, setDeletingAccount] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((currentUser) => {
      if (currentUser) {
        setUser(currentUser);
      } else {
        router.push('/login');
      }
      setLoading(false);
    });
    return () => unsubscribe();
  }, [router]);

  const handleSendVerification = async () => {
    setSendingVerification(true);
    setMessage('');
    setError('');

    try {
      await sendEmailVerification(user);
      setMessage('Verification email sent! Please check your inbox.');
    } catch {
      setError('Failed to send verification email.');
    } finally {
      setSendingVerification(false);
    }
  };

  const handleDeleteAccount = async () => {
    const confirmDelete = window.confirm(
      'Are you sure you want to delete your account? This action is irreversible and will delete all your data.'
    );
    if (!confirmDelete) return;

    setDeletingAccount(true);
    setMessage('');
    setError('');

    try {
      // Delete Firestore data
      await deleteDoc(doc(db, 'users', user.uid));

      // Delete Firebase Auth user
      await deleteUser(user);

      setMessage('Account deleted successfully.');
      router.push('/signup');
    } catch (err) {
      setError(
        err.code === 'auth/requires-recent-login'
          ? 'Please re-login and try again to delete your account.'
          : err.message || 'Failed to delete account.'
      );
    } finally {
      setDeletingAccount(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-lg text-gray-700 dark:text-gray-300">Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto mt-24 px-6 py-10 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-2xl shadow-lg">
      <h1 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-8">
        User Profile
      </h1>

      <div className="space-y-6">
        {/* Name */}
        <div className="flex justify-between">
          <p className="text-gray-600 dark:text-gray-300 font-medium">Name</p>
          <p className="text-gray-800 dark:text-gray-200">
            {user.displayName || 'Not set'}
          </p>
        </div>

        {/* Email */}
        <div className="flex justify-between">
          <p className="text-gray-600 dark:text-gray-300 font-medium">Email</p>
          <p className="text-gray-800 dark:text-gray-200">{user.email}</p>
        </div>

        {/* Email Status */}
        <div className="flex justify-between">
          <p className="text-gray-600 dark:text-gray-300 font-medium">Verification</p>
          <p
            className={`font-semibold ${
              user.emailVerified ? 'text-green-600' : 'text-rose-600'
            }`}
          >
            {user.emailVerified ? 'Verified' : 'Not Verified'}
          </p>
        </div>

        {/* Send Verification */}
        {!user.emailVerified && (
          <button
            onClick={handleSendVerification}
            disabled={sendingVerification}
            className="w-full py-3 rounded-lg bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white font-semibold transition disabled:opacity-60"
          >
            {sendingVerification ? 'Sending...' : 'Send Verification Email'}
          </button>
        )}

        {/* Messages */}
        {message && (
          <p className="text-center text-green-600 font-semibold">{message}</p>
        )}
        {error && (
          <p className="text-center text-rose-600 font-semibold">{error}</p>
        )}

        {/* Delete Button */}
        <button
          onClick={handleDeleteAccount}
          disabled={deletingAccount}
          className="w-full py-3 rounded-lg bg-rose-600 hover:bg-rose-700 text-white font-bold transition disabled:opacity-60 mt-6"
        >
          {deletingAccount ? 'Deleting...' : 'Delete Account'}
        </button>
      </div>
    </div>
  );
}
