/**
 * Auth callback handler for GitHub OAuth.
 *
 * Backend sets JWT cookie and redirects to /?auth=github.
 * This component calls refreshUser() and navigates home.
 */

import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

export function AuthCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { refreshUser } = useAuth();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleCallback = async () => {
      const errorParam = searchParams.get('error');
      if (errorParam) {
        setError(errorParam);
        return;
      }

      try {
        await refreshUser();
        const returnTo = sessionStorage.getItem('auth_return_to') || '/';
        sessionStorage.removeItem('auth_return_to');
        navigate(returnTo, { replace: true });
      } catch {
        setError('Authentication failed. Please try again.');
      }
    };

    handleCallback();
  }, [navigate, refreshUser, searchParams]);

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full p-6 bg-white rounded-lg shadow-md">
          <h1 className="text-2xl font-bold text-red-600 mb-4">Authentication Error</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/login')}
            className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-nordic-600 hover:bg-nordic-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-nordic-500"
          >
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-nordic-600 mx-auto mb-4" />
        <p className="text-gray-600">Completing authentication...</p>
      </div>
    </div>
  );
}

export default AuthCallback;
