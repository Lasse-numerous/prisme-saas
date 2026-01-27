/**
 * Login form component for Authentik OIDC.
 *
 * With Authentik OIDC, login is handled by redirecting to Authentik.
 * This component provides a login button that initiates the OIDC flow.
 */

import { useAuth } from '../../contexts/AuthContext';

export interface LoginFormProps {
  /** Called when user clicks signup link */
  onSignupClick?: () => void;
}

/**
 * Login component for Authentik OIDC authentication.
 * Redirects to Authentik for actual authentication.
 */
export function LoginForm({ onSignupClick }: LoginFormProps): JSX.Element {
  const { login, isLoading } = useAuth();

  const handleLogin = () => {
    login();
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white dark:bg-surface-elevated rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-nordic-800 dark:text-foreground mb-6 text-center">
          Sign In
        </h2>

        <p className="text-center text-nordic-600 dark:text-muted mb-6">
          Click the button below to sign in with your account.
        </p>

        <button
          onClick={handleLogin}
          disabled={isLoading}
          className="w-full bg-nordic-600 text-white py-2 px-4 rounded-md hover:bg-nordic-700 focus:outline-none focus:ring-2 focus:ring-nordic-500 focus:ring-offset-2 disabled:bg-nordic-300 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? 'Loading...' : 'Sign In with Authentik'}
        </button>

        {onSignupClick && (
          <div className="mt-6 text-center">
            <p className="text-sm text-nordic-600 dark:text-muted">
              Don't have an account?{' '}
              <button
                type="button"
                onClick={onSignupClick}
                className="text-nordic-600 hover:text-nordic-800 dark:text-primary dark:hover:text-primary-hover font-medium underline"
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
