/**
 * Login page for Authentik OIDC.
 *
 * With OIDC, login success is handled via the AuthCallback component.
 */

import { useNavigate } from 'react-router-dom';
import { LoginForm } from '../components/auth/LoginForm';

/**
 * Login page with OIDC redirect.
 */
export function Login(): JSX.Element {
  const navigate = useNavigate();

  const handleSignupClick = () => {
    navigate('/signup');
  };

  return (
    <div className="min-h-screen bg-nordic-50 dark:bg-surface flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <LoginForm onSignupClick={handleSignupClick} />
    </div>
  );
}
