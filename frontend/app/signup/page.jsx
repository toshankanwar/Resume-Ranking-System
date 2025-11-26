'use client';

import { useState, useEffect } from 'react';
import {
  createUserWithEmailAndPassword,
  sendEmailVerification,
  updateProfile,
  GoogleAuthProvider,
  signInWithPopup,
  onAuthStateChanged,
} from 'firebase/auth';
import { auth, db } from '@/lib/firebase';
import { doc, getDoc, setDoc, serverTimestamp } from 'firebase/firestore';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff } from 'lucide-react';

const GoogleLogo = () => (
  <svg className="w-5 h-5" viewBox="0 0 533.5 544.3" xmlns="http://www.w3.org/2000/svg">
    <path fill="#4285f4" d="M533.5 278.4c0-17.5-1.6-34.3-4.6-50.7H272v95.9h146.9c-6.4 35-26 64.7-55.5 84.7v70h89.7c52.3-48.2 82.4-119.1 82.4-199.9z"/>
    <path fill="#34a853" d="M272 544.3c74.4 0 136.8-24.6 182.4-66.9l-89.7-70c-24.9 16.7-57 26.4-92.7 26.4-71 0-131.2-47.9-152.8-112.2H26.4v70.3C71.7 491.7 166.6 544.3 272 544.3z"/>
    <path fill="#fbbc04" d="M119.2 324.6c-11.1-32.7-11.1-67.9 0-100.6V153.7H26.4c-39.1 76.5-39.1 167.8 0 244.3l92.8-73.4z"/>
    <path fill="#ea4335" d="M272 107.9c39.8 0 75.5 13.7 103.7 40.7l77.8-77.8C405.7 24.7 344 0 272 0 166.6 0 71.7 52.6 26.4 153.7l92.8 73.4c21.6-64.3 81.8-112.2 152.8-112.2z"/>
  </svg>
);

export default function SignupPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [info, setInfo] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  // Redirect logged-in users away from signup page
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) router.push('/dashboard');
    });
    return () => unsubscribe();
  }, [router]);

  // Simple utility to wait
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const handleSignup = async (e) => {
    e.preventDefault();
    setError('');
    setInfo('');

    if (password !== confirm) {
      setError('Passwords do not match.');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    setLoading(true);
    try {
      const cred = await createUserWithEmailAndPassword(auth, email, password);

      if (name.trim()) {
        await updateProfile(cred.user, { displayName: name.trim() });
      }

      await setDoc(doc(db, 'users', cred.user.uid), {
        email: cred.user.email,
        name: cred.user.displayName || '',
        createdAt: serverTimestamp(),
      });

      await sendEmailVerification(cred.user);

      setInfo('Account created. Verification email sent. Redirecting to dashboard...');

      await sleep(3000);

      router.push('/dashboard');
    } catch (err) {
      setError(err.message || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
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
      }

      // Delay for smooth UX before redirect
      setTimeout(() => router.push('/dashboard'), 1200);
    } catch (err) {
      setError(err.message || 'Google sign-in failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-6 py-12">
      <div className="w-full max-w-md bg-white dark:bg-gray-800 rounded-3xl shadow-lg p-10">
        <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-4 text-center">
          Create your recruiter account
        </h1>
        <p className="text-center text-gray-600 dark:text-gray-300 mb-8">
          Sign up to access your dashboard and manage all resume ranking sessions securely.
        </p>

        <button
          onClick={handleGoogleSignIn}
          disabled={loading}
          className="flex mx-auto mb-6 items-center gap-2 py-2 px-6 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 transition font-semibold text-lg shadow-sm"
          aria-label="Sign in with Google"
        >
          <GoogleLogo />
          {loading ? 'Signing in with Google...' : 'Sign in with Google'}
        </button>

        <div className="flex items-center mb-6">
          <hr className="flex-grow border-gray-300 dark:border-gray-500" />
          <span className="px-4 text-gray-500 dark:text-gray-400 font-semibold">or</span>
          <hr className="flex-grow border-gray-300 dark:border-gray-500" />
        </div>

        <form onSubmit={handleSignup} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Full name
            </label>
            <input
              type="text"
              placeholder="Your Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-3 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Email address
            </label>
            <input
              type="email"
              placeholder="you@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-3 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                placeholder="At least 6 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                minLength={6}
                required
                className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-3 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition pr-10"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition"
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Confirm password
            </label>
            <input
              type="password"
              placeholder="Re-enter password"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              required
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-3 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            />
          </div>

          {error && <p className="text-center text-sm text-red-600 font-semibold">{error}</p>}
          {info && <p className="text-center text-sm text-green-600 font-semibold">{info}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-primary-600 hover:bg-primary-700 disabled:bg-primary-400 disabled:cursor-not-allowed text-white font-semibold shadow-md transition"
          >
            {loading ? 'Creating account...' : 'Sign up'}
          </button>
        </form>

        <p className="mt-8 text-center text-xs text-gray-400 dark:text-gray-500">
          By signing up, you agree to receive a verification email. You must verify your email before accessing resume ranking features.
        </p>
      </div>
    </div>
  );
}
