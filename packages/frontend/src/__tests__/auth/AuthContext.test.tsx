import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import { AuthProvider, useAuth } from '../../contexts/AuthContext';

const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

// Helper to render a component that exposes auth state
function AuthConsumer() {
  const auth = useAuth();
  return (
    <div>
      <span data-testid="loading">{String(auth.isLoading)}</span>
      <span data-testid="authenticated">{String(auth.isAuthenticated)}</span>
      <span data-testid="email">{auth.user?.email ?? 'none'}</span>
      <button data-testid="logout" onClick={auth.logout}>Logout</button>
      <button data-testid="refresh" onClick={auth.refreshUser}>Refresh</button>
    </div>
  );
}

function renderWithAuth() {
  return render(
    <AuthProvider>
      <AuthConsumer />
    </AuthProvider>,
  );
}

beforeEach(() => {
  mockFetch.mockReset();
  // Reset window.location for public page tests
  Object.defineProperty(window, 'location', {
    value: { pathname: '/dashboard', href: '' },
    writable: true,
  });
});

describe('AuthContext', () => {
  it('shows authenticated user when /api/auth/me succeeds', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ id: 1, email: 'a@b.com', username: 'test', roles: ['user'], is_active: true }),
    });

    renderWithAuth();

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('true');
    });
    expect(screen.getByTestId('email').textContent).toBe('a@b.com');
  });

  it('shows unauthenticated when /api/auth/me returns 401', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 401,
      statusText: 'Unauthorized',
    });

    renderWithAuth();

    await waitFor(() => {
      expect(screen.getByTestId('loading').textContent).toBe('false');
    });
    expect(screen.getByTestId('authenticated').textContent).toBe('false');
  });

  it('skips auth check on public pages', async () => {
    Object.defineProperty(window, 'location', {
      value: { pathname: '/login', href: '' },
      writable: true,
    });

    renderWithAuth();

    await waitFor(() => {
      expect(screen.getByTestId('loading').textContent).toBe('false');
    });
    // fetch should NOT have been called
    expect(mockFetch).not.toHaveBeenCalled();
  });

  it('logout clears user state', async () => {
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({ id: 1, email: 'a@b.com', username: 'test', roles: ['user'], is_active: true }),
      })
      .mockResolvedValueOnce({ ok: true }); // logout POST

    renderWithAuth();

    await waitFor(() => {
      expect(screen.getByTestId('authenticated').textContent).toBe('true');
    });

    await act(async () => {
      screen.getByTestId('logout').click();
    });

    expect(screen.getByTestId('authenticated').textContent).toBe('false');
  });

  it('refreshUser re-fetches user', async () => {
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({ id: 1, email: 'old@b.com', username: 'test', roles: ['user'], is_active: true }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({ id: 1, email: 'new@b.com', username: 'test', roles: ['user'], is_active: true }),
      });

    renderWithAuth();

    await waitFor(() => {
      expect(screen.getByTestId('email').textContent).toBe('old@b.com');
    });

    await act(async () => {
      screen.getByTestId('refresh').click();
    });

    await waitFor(() => {
      expect(screen.getByTestId('email').textContent).toBe('new@b.com');
    });
  });
});
