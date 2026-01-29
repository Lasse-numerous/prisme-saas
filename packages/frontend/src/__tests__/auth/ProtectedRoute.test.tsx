import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { ProtectedRoute } from '../../components/auth/ProtectedRoute';

// Mock useAuth
const mockUseAuth = vi.fn();
vi.mock('../../contexts/AuthContext', () => ({
  useAuth: () => mockUseAuth(),
}));

function renderProtected(roles?: string[]) {
  return render(
    <MemoryRouter>
      <ProtectedRoute roles={roles}>
        <div data-testid="protected-content">Secret Content</div>
      </ProtectedRoute>
    </MemoryRouter>,
  );
}

describe('ProtectedRoute', () => {
  it('renders children when authenticated', () => {
    mockUseAuth.mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: { id: 1, roles: ['user'] },
    });

    renderProtected();
    expect(screen.getByTestId('protected-content')).toBeInTheDocument();
  });

  it('redirects when unauthenticated', () => {
    mockUseAuth.mockReturnValue({
      isAuthenticated: false,
      isLoading: false,
      user: null,
    });

    renderProtected();
    expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();
  });

  it('blocks without required role', () => {
    mockUseAuth.mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: { id: 1, roles: ['user'] },
    });

    renderProtected(['admin']);
    expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();
    expect(screen.getByText('403')).toBeInTheDocument();
  });

  it('allows with required role', () => {
    mockUseAuth.mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: { id: 1, roles: ['admin'] },
    });

    renderProtected(['admin']);
    expect(screen.getByTestId('protected-content')).toBeInTheDocument();
  });
});
