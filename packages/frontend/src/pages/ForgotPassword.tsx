/**
 * Forgot password page.
 */

import { useNavigate } from 'react-router-dom';
import { ForgotPasswordForm } from '../components/auth/ForgotPasswordForm';

export function ForgotPassword(): JSX.Element {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-nordic-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <ForgotPasswordForm
        onSuccess={() => navigate('/', { replace: true })}
        onBackToLogin={() => navigate('/login')}
      />
    </div>
  );
}
