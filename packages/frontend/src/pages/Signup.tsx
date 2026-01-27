/**
 * Signup page for Authentik OIDC.
 *
 * With OIDC, signup success is handled via the AuthCallback component.
 */

import { useNavigate } from 'react-router-dom';
import { SignupForm } from '../components/auth/SignupForm';

/**
 * Signup page with OIDC redirect.
 */
export function Signup(): JSX.Element {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-nordic-50 dark:bg-surface flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <SignupForm onLoginClick={handleLoginClick} />
    </div>
  );
}
