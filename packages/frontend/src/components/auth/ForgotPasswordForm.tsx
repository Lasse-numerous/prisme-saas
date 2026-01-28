/**
 * Forgot password form driving the Authentik recovery flow.
 *
 * Steps: email identification -> email sent confirmation -> (user clicks link) -> new password -> done
 */

import React, { useCallback, useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import {
  startRecoveryFlow,
  submitRecoveryFlow,
  type FlowChallenge,
} from '../../lib/authApi';

export interface ForgotPasswordFormProps {
  onSuccess?: () => void;
  onBackToLogin?: () => void;
}

type RecoveryStep = 'email' | 'email_sent' | 'new_password' | 'complete';

export function ForgotPasswordForm({ onSuccess, onBackToLogin }: ForgotPasswordFormProps): JSX.Element {
  const { refreshUser } = useAuth();
  const [flowToken, setFlowToken] = useState<string | null>(null);
  const [step, setStep] = useState<RecoveryStep>('email');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const [initError, setInitError] = useState(false);
  const [challenge, setChallenge] = useState<FlowChallenge | null>(null);

  const initFlow = useCallback(async () => {
    setInitializing(true);
    setInitError(false);
    try {
      const result = await startRecoveryFlow();
      setFlowToken(result.flow_token);
      setChallenge(result.challenge);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize recovery');
      setInitError(true);
    } finally {
      setInitializing(false);
    }
  }, []);

  useEffect(() => {
    initFlow();
  }, [initFlow]);

  const handleSubmitEmail = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!flowToken) return;
    setError(null);
    setLoading(true);

    try {
      const result = await submitRecoveryFlow(flowToken, { uid_field: email });

      if (result.error) {
        setError(result.error);
        setLoading(false);
        return;
      }

      if (result.completed) {
        setStep('complete');
        if (result.user) {
          await refreshUser();
          onSuccess?.();
        }
        setLoading(false);
        return;
      }

      // Next challenge — likely email verification or password reset
      if (result.challenge) {
        setChallenge(result.challenge);
        if (result.challenge.type === 'email_verification' || result.challenge.type === 'email') {
          setStep('email_sent');
        } else if (result.challenge.type === 'password') {
          setStep('new_password');
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Recovery failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitNewPassword = async (e: React.FormEvent) => {
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
        setStep('complete');
        if (result.user) {
          await refreshUser();
          onSuccess?.();
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset password');
    } finally {
      setLoading(false);
    }
  };

  if (initializing) {
    return (
      <div className="w-full max-w-md mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-nordic-600 mx-auto mb-4" />
          <p className="text-nordic-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (initError) {
    return (
      <div className="w-full max-w-md mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={initFlow}
            className="bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 transition-colors"
          >
            Try again
          </button>
          {onBackToLogin && (
            <button
              onClick={onBackToLogin}
              className="block mx-auto mt-3 text-sm text-nordic-600 hover:text-nordic-800 underline"
            >
              Back to login
            </button>
          )}
        </div>
      </div>
    );
  }

  if (step === 'complete') {
    return (
      <div className="w-full max-w-md mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <h2 className="text-2xl font-bold text-nordic-800 mb-4">Password Reset</h2>
          <p className="text-nordic-600 mb-6">
            Your password has been reset successfully.
          </p>
          {onBackToLogin && (
            <button
              onClick={onBackToLogin}
              className="bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 transition-colors"
            >
              Back to login
            </button>
          )}
        </div>
      </div>
    );
  }

  if (step === 'email_sent') {
    return (
      <div className="w-full max-w-md mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <h2 className="text-2xl font-bold text-nordic-800 mb-4">Check Your Email</h2>
          <p className="text-nordic-600 mb-6">
            If an account exists for <strong>{email}</strong>, we've sent a password reset link.
            Please check your inbox and follow the instructions.
          </p>
          {onBackToLogin && (
            <button
              onClick={onBackToLogin}
              className="text-sm text-nordic-600 hover:text-nordic-800 underline"
            >
              Back to login
            </button>
          )}
        </div>
      </div>
    );
  }

  if (step === 'new_password') {
    return (
      <div className="w-full max-w-md mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-nordic-800 mb-6 text-center">Set New Password</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmitNewPassword} className="space-y-4">
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
    );
  }

  // Default: email input step
  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-nordic-800 mb-2 text-center">Forgot Password</h2>
        <p className="text-sm text-nordic-600 text-center mb-6">
          Enter your email address and we'll send you a link to reset your password.
        </p>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmitEmail} className="space-y-4">
          <div>
            <label htmlFor="recovery-email" className="block text-sm font-medium text-nordic-700 mb-1">
              Email
            </label>
            <input
              type="email"
              id="recovery-email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
              className="w-full px-3 py-2 border border-nordic-200 rounded-md focus:outline-none focus:ring-2 focus:ring-nordic-500 disabled:bg-nordic-50 disabled:cursor-not-allowed"
              placeholder="Enter your email"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 focus:outline-none focus:ring-2 focus:ring-nordic-500 focus:ring-offset-2 disabled:bg-nordic-300 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Sending...' : 'Send Reset Link'}
          </button>
        </form>

        {onBackToLogin && (
          <div className="mt-6 text-center">
            <button
              type="button"
              onClick={onBackToLogin}
              className="text-sm text-nordic-600 hover:text-nordic-800 font-medium underline"
            >
              Back to login
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
