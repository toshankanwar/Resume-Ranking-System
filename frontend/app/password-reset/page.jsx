'use client';

import { useState } from 'react';
import { auth } from '@/lib/firebase';
import { sendPasswordResetEmail } from 'firebase/auth';

export default function PasswordReset() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleReset = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    setLoading(true);

    try {
      await sendPasswordResetEmail(auth, email);
      setMessage('Password reset email sent! Check your inbox.');
    } catch (err) {
      setError(err.message || 'Failed to send reset email.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-start justify-center bg-gray-100 dark:bg-gray-900 px-6 pt-24">
      {/* Small pt-24 (instead of big margin) keeps it close to header */}
      <div className="w-full max-w-md bg-gray-100 dark:bg-gray-900 rounded-xl shadow-md p-8">

        <h2 className="text-3xl font-bold mb-6 text-center text-gray-900 dark:text-white">
          Reset Password
        </h2>

        <form onSubmit={handleReset} className="space-y-5">

          {/* Email Input */}
          <div>
            <label className="block mb-2 text-sm font-semibold text-gray-800 dark:text-gray-200">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              className="w-full rounded-lg border border-gray-300 dark:border-gray-700 
                         bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white 
                         px-4 py-3 placeholder-gray-400 
                         focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
            />
          </div>

          {/* Success & Error */}
          {message && (
            <p className="text-green-600 text-center font-semibold">{message}</p>
          )}
          {error && (
            <p className="text-red-600 text-center font-semibold">{error}</p>
          )}

          {/* Reset Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-lg bg-purple-600 hover:bg-purple-700 
                       text-white font-semibold transition disabled:opacity-60"
          >
            {loading ? 'Sending...' : 'Send Reset Link'}
          </button>
        </form>
      </div>
    </div>
  );
}
