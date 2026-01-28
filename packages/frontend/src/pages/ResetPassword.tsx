/**
 * Reset password page — receives token from email link,
 * verifies it via the backend, and shows the password form.
 */

import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  verifyRecoveryToken,
  submitRecoveryFlow,
} from '../lib/authApi';

export default function ResetPassword(): JSX.Element {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const { refreshUser } = useAuth();

  const [flowToken, setFlowToken] = useState<string | null>(null);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [verifying, setVerifying] = useState(true);
  const [verifyFailed, setVerifyFailed] = useState(false);
  const [complete, setComplete] = useState(false);

  const verifyToken = useCallback(async () => {
    if (!token) {
      setError('No reset token provided');
      setVerifyFailed(true);
      setVerifying(false);
      return;
    }

    setVerifying(true);
    setVerifyFailed(false);
    setError(null);

    try {
      const result = await verifyRecoveryToken(token);
      setFlowToken(result.flow_token);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid or expired reset link');
      setVerifyFailed(true);
    } finally {
      setVerifying(false);
    }
  }, [token]);

  useEffect(() => {
    verifyToken();
  }, [verifyToken]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!flowToken) return;

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const result = await submitRecoveryFlow(flowToken, { password });

      if (result.error) {
        setError(result.error);
        setLoading(false);
        return;
      }

      if (result.completed) {
        setComplete(true);
        if (result.user) {
          await refreshUser();
          navigate('/', { replace: true });
          return;
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset password');
    } finally {
      setLoading(false);
    }
  };

  if (verifying) {
    return (
      <div className="min-h-screen bg-nordic-50 flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-nordic-600 mx-auto mb-4" />
            <p className="text-nordic-600">Verifying reset link...</p>
          </div>
        </div>
      </div>
    );
  }

  if (verifyFailed) {
    return (
      <div className="min-h-screen bg-nordic-50 flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <h2 className="text-2xl font-bold text-nordic-800 mb-4">Invalid Reset Link</h2>
            <p className="text-red-600 mb-6">{error}</p>
            <button
              onClick={() => navigate('/forgot-password')}
              className="bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 transition-colors"
            >
              Request a new reset link
            </button>
            <button
              onClick={() => navigate('/login')}
              className="block mx-auto mt-3 text-sm text-nordic-600 hover:text-nordic-800 underline"
            >
              Back to login
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (complete) {
    return (
      <div className="min-h-screen bg-nordic-50 flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <h2 className="text-2xl font-bold text-nordic-800 mb-4">Password Reset</h2>
            <p className="text-nordic-600 mb-6">Your password has been reset successfully.</p>
            <button
              onClick={() => navigate('/login')}
              className="bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 transition-colors"
            >
              Back to login
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-nordic-50 flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-md mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-nordic-800 mb-6 text-center">Set New Password</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-nordic-700 mb-1">
                New Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
                className="w-full px-3 py-2 border border-nordic-200 rounded-md focus:outline-none focus:ring-2 focus:ring-nordic-500 disabled:bg-nordic-50 disabled:cursor-not-allowed"
                placeholder="Enter new password"
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-nordic-700 mb-1">
                Confirm Password
              </label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                disabled={loading}
                className="w-full px-3 py-2 border border-nordic-200 rounded-md focus:outline-none focus:ring-2 focus:ring-nordic-500 disabled:bg-nordic-50 disabled:cursor-not-allowed"
                placeholder="Confirm new password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 focus:outline-none focus:ring-2 focus:ring-nordic-500 focus:ring-offset-2 disabled:bg-nordic-300 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Resetting...' : 'Reset Password'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
