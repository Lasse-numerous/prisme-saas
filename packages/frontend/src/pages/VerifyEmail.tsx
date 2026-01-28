/**
 * Email verification page — receives token from signup email link,
 * verifies it via the backend, and shows the result.
 */

import { useCallback, useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { verifyEmailToken } from '../lib/authApi';

export default function VerifyEmail(): JSX.Element {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [error, setError] = useState<string | null>(null);
  const [verifying, setVerifying] = useState(true);
  const [verified, setVerified] = useState(false);

  const verify = useCallback(async () => {
    if (!token) {
      setError('No verification token provided');
      setVerifying(false);
      return;
    }

    setVerifying(true);
    setError(null);

    try {
      await verifyEmailToken(token);
      setVerified(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid or expired verification link');
    } finally {
      setVerifying(false);
    }
  }, [token]);

  useEffect(() => {
    verify();
  }, [verify]);

  if (verifying) {
    return (
      <div className="min-h-screen bg-nordic-50 flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-nordic-600 mx-auto mb-4" />
            <p className="text-nordic-600">Verifying your email...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-nordic-50 flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <h2 className="text-2xl font-bold text-nordic-800 mb-4">Verification Failed</h2>
            <p className="text-red-600 mb-6">{error}</p>
            <button
              onClick={() => navigate('/login')}
              className="bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 transition-colors"
            >
              Go to login
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-nordic-50 flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-md mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <h2 className="text-2xl font-bold text-nordic-800 mb-4">Email Verified</h2>
          <p className="text-nordic-600 mb-6">
            Your email has been verified successfully. You can now log in.
          </p>
          <button
            onClick={() => navigate('/login')}
            className="bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 transition-colors"
          >
            Go to login
          </button>
        </div>
      </div>
    </div>
  );
}
