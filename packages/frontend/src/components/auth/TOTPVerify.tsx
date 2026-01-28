/**
 * TOTP verification input for MFA login step.
 */

import React, { useState, useRef, useEffect } from 'react';

export interface TOTPVerifyProps {
  onSubmit: (code: string) => void;
  error?: string | null;
  loading?: boolean;
}

export function TOTPVerify({ onSubmit, error, loading }: TOTPVerifyProps) {
  const [code, setCode] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (code.length === 6) {
      onSubmit(code);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.replace(/\D/g, '').slice(0, 6);
    setCode(value);
    if (value.length === 6) {
      onSubmit(value);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-nordic-800 mb-2 text-center">
          Two-Factor Authentication
        </h2>
        <p className="text-nordic-600 text-center mb-6">
          Enter the 6-digit code from your authenticator app.
        </p>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <input
            ref={inputRef}
            type="text"
            inputMode="numeric"
            autoComplete="one-time-code"
            value={code}
            onChange={handleChange}
            maxLength={6}
            disabled={loading}
            className="w-full text-center text-3xl tracking-[0.5em] px-3 py-4 border border-nordic-200 rounded-md focus:outline-none focus:ring-2 focus:ring-nordic-500 disabled:bg-nordic-50 disabled:cursor-not-allowed font-mono"
            placeholder="------"
          />

          <button
            type="submit"
            disabled={loading || code.length !== 6}
            className="w-full mt-4 bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 focus:outline-none focus:ring-2 focus:ring-nordic-500 focus:ring-offset-2 disabled:bg-nordic-300 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Verifying...' : 'Verify'}
          </button>
        </form>
      </div>
    </div>
  );
}
