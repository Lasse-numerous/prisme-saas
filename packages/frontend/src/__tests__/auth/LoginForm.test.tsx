import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from '../../components/auth/LoginForm';

// Mock AuthContext
vi.mock('../../contexts/AuthContext', () => ({
  useAuth: () => ({
    refreshUser: vi.fn(),
  }),
}));

// Mock authApi
const mockLogin = vi.fn();
const mockLoginMFA = vi.fn();
vi.mock('../../lib/authApi', () => ({
  login: (...args: unknown[]) => mockLogin(...args),
  loginMFA: (...args: unknown[]) => mockLoginMFA(...args),
  getGitHubLoginUrl: () => '/api/auth/github/login',
}));

beforeEach(() => {
  mockLogin.mockReset();
  mockLoginMFA.mockReset();
});

describe('LoginForm', () => {
  it('renders email and password fields', () => {
    render(<LoginForm />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it('submits credentials', async () => {
    mockLogin.mockResolvedValue({ requires_mfa: false, user: { id: 1 } });
    const user = userEvent.setup();
    render(<LoginForm />);

    await user.type(screen.getByLabelText(/email/i), 'a@b.com');
    await user.type(screen.getByLabelText(/password/i), 'Pass1234');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('a@b.com', 'Pass1234');
    });
  });

  it('shows error on failure', async () => {
    mockLogin.mockRejectedValue(new Error('Invalid email or password.'));
    const user = userEvent.setup();
    render(<LoginForm />);

    await user.type(screen.getByLabelText(/email/i), 'a@b.com');
    await user.type(screen.getByLabelText(/password/i), 'wrong');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText(/invalid email or password/i)).toBeInTheDocument();
    });
  });

  it('shows MFA step when required', async () => {
    mockLogin.mockResolvedValue({ requires_mfa: true });
    const user = userEvent.setup();
    render(<LoginForm />);

    await user.type(screen.getByLabelText(/email/i), 'a@b.com');
    await user.type(screen.getByLabelText(/password/i), 'Pass1234');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText(/two-factor authentication/i)).toBeInTheDocument();
    });
  });

  it('renders GitHub login link', () => {
    render(<LoginForm />);
    expect(screen.getByText(/sign in with github/i)).toBeInTheDocument();
  });
});
