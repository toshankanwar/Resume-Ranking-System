'use client';

import { useState } from 'react';
import {
  signInWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup,
} from 'firebase/auth';
import { auth, db } from '@/lib/firebase';
import { useRouter } from 'next/navigation';
import { doc, getDoc, setDoc, serverTimestamp } from 'firebase/firestore';
import { Eye, EyeOff } from 'lucide-react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [info, setInfo] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleEmailLogin = async (e) => {
    e.preventDefault();
    setError('');
    setInfo('');
    setLoading(true);

    try {
      await signInWithEmailAndPassword(auth, email, password);
      router.push('/dashboard');
    } catch {
      setError('Wrong email or password');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    setError('');
    setInfo('');
    setLoading(true);

    try {
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(auth, provider);
      const user = result.user;

      const userRef = doc(db, 'users', user.uid);
      const snap = await getDoc(userRef);

      if (!snap.exists()) {
        await setDoc(userRef, {
          email: user.email,
          name: user.displayName || '',
          createdAt: serverTimestamp(),
        });
        setTimeout(() => router.push('/dashboard'), 1500);
      } else {
        setTimeout(() => router.push('/dashboard'), 1000);
      }
    } catch (err) {
      setError(err.message || 'Google sign-in failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 px-6 py-12">
      <div className="w-full max-w-md bg-white dark:bg-gray-800 rounded-3xl shadow-lg p-10">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-8">
          Login to Your Account
        </h1>

        <form onSubmit={handleEmailLogin} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Email
            </label>
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white px-4 py-3 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 transition"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white px-4 py-3 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 pr-10 transition"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition"
                tabIndex={-1}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          {error && <p className="text-red-600 text-center text-sm font-medium">{error}</p>}
          {info && <p className="text-green-600 text-center text-sm font-medium">{info}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-primary-600 text-white rounded-xl font-semibold hover:bg-primary-700 disabled:bg-primary-400 disabled:cursor-not-allowed transition-shadow shadow-md"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="mt-8 flex items-center justify-center gap-4">
          <hr className="flex-grow border-gray-300 dark:border-gray-700" />
          <span className="text-gray-500 dark:text-gray-400 font-semibold">or</span>
          <hr className="flex-grow border-gray-300 dark:border-gray-700" />
        </div>

        <button
          onClick={handleGoogleLogin}
          disabled={loading}
          className="w-full mt-6 flex items-center justify-center gap-3 py-3 border rounded-xl border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white bg-white dark:bg-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 font-semibold shadow-md transition"
          aria-label="Sign in with Google"
        >
          <svg className="w-6 h-6" viewBox="0 0 533.5 544.3" xmlns="http://www.w3.org/2000/svg" fill="none">
            <path fill="#4285f4" d="M533.5 278.4c0-17.5-1.6-34.3-4.6-50.7H272v95.9h146.9c-6.4 35-26 64.7-55.5 84.7v70h89.7c52.3-48.2 82.4-119.1 82.4-199.9z" />
            <path fill="#34a853" d="M272 544.3c74.4 0 136.8-24.6 182.4-66.9l-89.7-70c-24.9 16.7-57 26.4-92.7 26.4-71 0-131.2-47.9-152.8-112.2H26.4v70.3C71.7 491.7 166.6 544.3 272 544.3z" />
            <path fill="#fbbc04" d="M119.2 324.6c-11.1-32.7-11.1-67.9 0-100.6V153.7H26.4c-39.1 76.5-39.1 167.8 0 244.3l92.8-73.4z" />
            <path fill="#ea4335" d="M272 107.9c39.8 0 75.5 13.7 103.7 40.7l77.8-77.8C405.7 24.7 344 0 272 0 166.6 0 71.7 52.6 26.4 153.7l92.8 73.4c21.6-64.3 81.8-112.2 152.8-112.2z" />
          </svg>
          Sign in with Google
        </button>
      </div>
    </div>
  );
}
