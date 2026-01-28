/**
 * TOTP setup component with QR code display.
 * Used in user settings to enable MFA.
 */

import React, { useState } from 'react';

export interface TOTPSetupProps {
  totpUrl: string;
  onVerify: (code: string) => void;
  error?: string | null;
  loading?: boolean;
}

export function TOTPSetup({ totpUrl, onVerify, error, loading }: TOTPSetupProps) {
  const [code, setCode] = useState('');

  // Generate QR code URL using a public API (no dependency needed)
  const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(totpUrl)}`;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (code.length === 6) {
      onVerify(code);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-nordic-800 mb-2 text-center">
          Set Up Two-Factor Authentication
        </h2>
        <p className="text-nordic-600 text-center mb-6">
          Scan this QR code with your authenticator app, then enter the verification code.
        </p>

        <div className="flex justify-center mb-6">
          <img
            src={qrCodeUrl}
            alt="TOTP QR Code"
            className="w-48 h-48 border border-nordic-200 rounded-md"
          />
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <label htmlFor="totp-code" className="block text-sm font-medium text-nordic-700 mb-1">
            Verification Code
          </label>
          <input
            id="totp-code"
            type="text"
            inputMode="numeric"
            autoComplete="one-time-code"
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
            maxLength={6}
            disabled={loading}
            className="w-full text-center text-xl tracking-widest px-3 py-2 border border-nordic-200 rounded-md focus:outline-none focus:ring-2 focus:ring-nordic-500 disabled:bg-nordic-50 font-mono mb-4"
            placeholder="000000"
          />

          <button
            type="submit"
            disabled={loading || code.length !== 6}
            className="w-full bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 focus:outline-none focus:ring-2 focus:ring-nordic-500 focus:ring-offset-2 disabled:bg-nordic-300 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Verifying...' : 'Enable Two-Factor Authentication'}
          </button>
        </form>
      </div>
    </div>
  );
}
