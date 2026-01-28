/**
 * Login page.
 *
 * Reads ?error= query param (from OAuth failures) and location.state.from (for redirect after login).
 */

import React from 'react';
import { useNavigate, useLocation, useSearchParams } from 'react-router-dom';
import { LoginForm } from '../components/auth/LoginForm';

const ERROR_MESSAGES: Record<string, string> = {
  missing_params: 'Authentication failed: missing parameters.',
  invalid_state: 'Authentication failed: invalid state. Please try again.',
  token_exchange_failed: 'Authentication failed: could not exchange token.',
  no_access_token: 'Authentication failed: no access token received.',
  github_user_failed: 'Authentication failed: could not retrieve GitHub user.',
  no_email: 'Authentication failed: no email associated with your GitHub account.',
};

/**
 * Login page with form and navigation.
 */
export function Login(): JSX.Element {
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams] = useSearchParams();

  // Get the page user was trying to access before login
  const from = (location.state as any)?.from?.pathname || '/';

  // Read OAuth error from query param
  const errorParam = searchParams.get('error');
  const externalError = errorParam
    ? ERROR_MESSAGES[errorParam] || `Authentication error: ${errorParam}`
    : null;

  const handleSuccess = () => {
    navigate(from, { replace: true });
  };

  const handleSignupClick = () => {
    navigate('/signup');
  };

  const handleForgotPasswordClick = () => {
    navigate('/forgot-password');
  };

  return (
    <div className="min-h-screen bg-nordic-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <LoginForm
        onSuccess={handleSuccess}
        onSignupClick={handleSignupClick}
        onForgotPasswordClick={handleForgotPasswordClick}
        externalError={externalError}
      />
    </div>
  );
}
