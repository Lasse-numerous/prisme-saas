/**
 * Signup form component for Authentik OIDC.
 *
 * With Authentik OIDC, signup is handled by Authentik's self-registration.
 * This component provides a signup button that initiates the OIDC flow.
 */

import { useAuth } from '../../contexts/AuthContext';

export interface SignupFormProps {
  /** Called when user clicks login link */
  onLoginClick?: () => void;
}

/** API base URL from environment */
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

/**
 * Signup component for Authentik OIDC authentication.
 * Redirects to Authentik for self-registration.
 */
export function SignupForm({ onLoginClick }: SignupFormProps): JSX.Element {
  const { isLoading } = useAuth();

  const handleSignup = () => {
    // Redirect to Authentik signup/registration flow
    // This is typically the same as login, but Authentik shows a "register" option
    window.location.href = `${API_BASE_URL}/api/auth/login`;
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white dark:bg-surface-elevated rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-nordic-800 dark:text-foreground mb-6 text-center">
          Create Account
        </h2>

        <p className="text-center text-nordic-600 dark:text-muted mb-6">
          Click the button below to create a new account.
          You'll be redirected to our secure authentication provider.
        </p>

        <button
          onClick={handleSignup}
          disabled={isLoading}
          className="w-full bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 focus:outline-none focus:ring-2 focus:ring-nordic-500 focus:ring-offset-2 disabled:bg-nordic-300 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? 'Loading...' : 'Sign Up with Authentik'}
        </button>

        {onLoginClick && (
          <div className="mt-6 text-center">
            <p className="text-sm text-nordic-600 dark:text-muted">
              Already have an account?{' '}
              <button
                type="button"
                onClick={onLoginClick}
                className="text-nordic-600 hover:text-nordic-800 dark:text-primary dark:hover:text-primary-hover font-medium underline"
              >
                Sign in
              </button>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
