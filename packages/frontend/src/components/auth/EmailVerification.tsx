/**
 * Email verification pending screen.
 * Shown after signup when Authentik sends a verification email.
 */

import { useState } from 'react';

export interface EmailVerificationProps {
  onResend: () => Promise<void>;
  onBackToLogin: () => void;
}

export function EmailVerification({ onResend, onBackToLogin }: EmailVerificationProps) {
  const [resending, setResending] = useState(false);
  const [resent, setResent] = useState(false);

  const handleResend = async () => {
    setResending(true);
    setResent(false);
    try {
      await onResend();
      setResent(true);
    } catch {
      // silently fail
    } finally {
      setResending(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8 text-center">
        <div className="w-16 h-16 bg-nordic-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-nordic-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>

        <h2 className="text-2xl font-bold text-nordic-800 mb-2">Check your email</h2>
        <p className="text-nordic-600 mb-6">
          We sent a verification link to your email address. Click the link to activate your account.
        </p>

        {resent && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md">
            <p className="text-sm text-green-800">Verification email resent.</p>
          </div>
        )}

        <button
          type="button"
          onClick={handleResend}
          disabled={resending}
          className="text-sm text-nordic-600 hover:text-nordic-800 font-medium underline disabled:opacity-50"
        >
          {resending ? 'Sending...' : 'Resend verification email'}
        </button>

        <div className="mt-6">
          <button
            type="button"
            onClick={onBackToLogin}
            className="text-sm text-nordic-500 hover:text-nordic-700"
          >
            Back to login
          </button>
        </div>
      </div>
    </div>
  );
}
