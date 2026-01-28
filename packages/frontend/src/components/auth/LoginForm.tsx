/**
 * Login form with multi-step Authentik flow support.
 *
 * Single-screen layout: email + password together, GitHub button below.
 * If MFA is configured, shows TOTP input after password step.
 * If email not verified, shows error with resend link.
 */

import React, { useCallback, useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import {
  getGitHubLoginUrl,
  startLoginFlow,
  submitLoginFlow,
  type FlowChallenge,
} from '../../lib/authApi';
import { TOTPVerify } from './TOTPVerify';

export interface LoginFormProps {
  onSuccess?: () => void;
  onSignupClick?: () => void;
}

type LoginStep = 'credentials' | 'totp' | 'error';

export function LoginForm({ onSuccess, onSignupClick }: LoginFormProps): JSX.Element {
  const { refreshUser } = useAuth();
  const [flowToken, setFlowToken] = useState<string | null>(null);
  const [step, setStep] = useState<LoginStep>('credentials');
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const [challenge, setChallenge] = useState<FlowChallenge | null>(null);

  const initFlow = useCallback(async () => {
    setInitializing(true);
    try {
      const result = await startLoginFlow();
      setFlowToken(result.flow_token);
      setChallenge(result.challenge);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize login');
    } finally {
      setInitializing(false);
    }
  }, []);

  useEffect(() => {
    initFlow();
  }, [initFlow]);

  const handleSubmitCredentials = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!flowToken) return;
    setError(null);
    setLoading(true);

    try {
      // Submit identification (email/username)
      let result = await submitLoginFlow(flowToken, {
        uid_field: formData.email,
      });

      if (result.error) {
        setError(result.error);
        setLoading(false);
        return;
      }

      // If the next challenge is password, submit it immediately
      if (!result.completed && result.challenge?.type === 'password') {
        result = await submitLoginFlow(flowToken, {
          password: formData.password,
        });

        if (result.error) {
          setError(result.error);
          setLoading(false);
          return;
        }
      }

      // Check if we need TOTP
      if (!result.completed && result.challenge?.type === 'totp_verify') {
        setChallenge(result.challenge);
        setStep('totp');
        setLoading(false);
        return;
      }

      // Check if email verification needed
      if (!result.completed && result.challenge?.type === 'email_verification') {
        setError('Please verify your email before logging in.');
        setLoading(false);
        return;
      }

      if (result.completed) {
        await refreshUser();
        onSuccess?.();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleTOTPSubmit = async (code: string) => {
    if (!flowToken) return;
    setError(null);
    setLoading(true);

    try {
      const result = await submitLoginFlow(flowToken, { code });

      if (result.error) {
        setError(result.error);
        setLoading(false);
        return;
      }

      if (result.completed) {
        await refreshUser();
        onSuccess?.();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Verification failed');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
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

  if (step === 'totp') {
    return <TOTPVerify onSubmit={handleTOTPSubmit} error={error} loading={loading} />;
  }

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-nordic-800 mb-6 text-center">Sign In</h2>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmitCredentials} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-nordic-700 mb-1">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              disabled={loading}
              className="w-full px-3 py-2 border border-nordic-200 rounded-md focus:outline-none focus:ring-2 focus:ring-nordic-500 disabled:bg-nordic-50 disabled:cursor-not-allowed"
              placeholder="Enter your email"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-nordic-700 mb-1">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              disabled={loading}
              className="w-full px-3 py-2 border border-nordic-200 rounded-md focus:outline-none focus:ring-2 focus:ring-nordic-500 disabled:bg-nordic-50 disabled:cursor-not-allowed"
              placeholder="Enter your password"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 focus:outline-none focus:ring-2 focus:ring-nordic-500 focus:ring-offset-2 disabled:bg-nordic-300 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        {/* GitHub login */}
        <div className="mt-4">
          <div className="relative mb-4">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-nordic-200" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-nordic-500">or</span>
            </div>
          </div>

          <a
            href={getGitHubLoginUrl()}
            className="w-full flex items-center justify-center gap-2 bg-nordic-800 text-white py-2 px-4 rounded-md hover:bg-nordic-900 transition-colors"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
            </svg>
            Sign in with GitHub
          </a>
        </div>

        {onSignupClick && (
          <div className="mt-6 text-center">
            <p className="text-sm text-nordic-600">
              Don&apos;t have an account?{' '}
              <button
                type="button"
                onClick={onSignupClick}
                className="text-nordic-600 hover:text-nordic-800 font-medium underline"
              >
                Sign up
              </button>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
