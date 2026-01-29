import { describe, it, expect, vi, beforeEach } from 'vitest';
import {
  signup,
  login,
  loginMFA,
  verifyEmail,
  forgotPassword,
  resetPassword,
  setupMFA,
  verifyMFASetup,
  disableMFA,
} from '../../lib/authApi';

const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

function mockOk(data: unknown) {
  mockFetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve(data),
  });
}

function mockError(status: number, detail: string) {
  mockFetch.mockResolvedValueOnce({
    ok: false,
    status,
    json: () => Promise.resolve({ detail }),
  });
}

beforeEach(() => {
  mockFetch.mockReset();
});

describe('authApi', () => {
  it('signup calls POST /api/auth/signup', async () => {
    mockOk({ message: 'Account created.' });
    const result = await signup('a@b.com', 'user', 'Pass1234');
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/auth/signup',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ email: 'a@b.com', username: 'user', password: 'Pass1234' }),
      }),
    );
    expect(result.message).toBeDefined();
  });

  it('login calls POST /api/auth/login', async () => {
    mockOk({ requires_mfa: false, user: { id: 1 } });
    const result = await login('a@b.com', 'Pass1234');
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/auth/login',
      expect.objectContaining({ method: 'POST' }),
    );
    expect(result.requires_mfa).toBe(false);
  });

  it('loginMFA calls POST /api/auth/login/mfa', async () => {
    mockOk({ requires_mfa: false, user: { id: 1 } });
    await loginMFA('a@b.com', '123456');
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/auth/login/mfa',
      expect.objectContaining({
        body: JSON.stringify({ email: 'a@b.com', code: '123456' }),
      }),
    );
  });

  it('verifyEmail calls POST /api/auth/verify-email', async () => {
    mockOk({ message: 'Email verified', user: {} });
    await verifyEmail('tok123');
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/auth/verify-email',
      expect.objectContaining({
        body: JSON.stringify({ token: 'tok123' }),
      }),
    );
  });

  it('forgotPassword calls POST /api/auth/forgot-password', async () => {
    mockOk({ message: 'ok' });
    await forgotPassword('a@b.com');
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/auth/forgot-password',
      expect.objectContaining({
        body: JSON.stringify({ email: 'a@b.com' }),
      }),
    );
  });

  it('resetPassword calls POST /api/auth/reset-password', async () => {
    mockOk({ message: 'Password reset', user: {} });
    await resetPassword('tok', 'NewPass1');
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/auth/reset-password',
      expect.objectContaining({
        body: JSON.stringify({ token: 'tok', password: 'NewPass1' }),
      }),
    );
  });

  it('setupMFA calls POST /api/auth/mfa/setup', async () => {
    mockOk({ totp_uri: 'otpauth://...', secret: 'ABC' });
    const result = await setupMFA();
    expect(result.totp_uri).toBeDefined();
    expect(result.secret).toBe('ABC');
  });

  it('verifyMFASetup calls POST /api/auth/mfa/verify-setup', async () => {
    mockOk({ message: 'MFA enabled' });
    await verifyMFASetup('123456');
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/auth/mfa/verify-setup',
      expect.objectContaining({
        body: JSON.stringify({ code: '123456' }),
      }),
    );
  });

  it('disableMFA calls POST /api/auth/mfa/disable', async () => {
    mockOk({ message: 'MFA disabled' });
    await disableMFA('mypassword');
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/auth/mfa/disable',
      expect.objectContaining({
        body: JSON.stringify({ password: 'mypassword' }),
      }),
    );
  });

  it('throws on error response', async () => {
    mockError(401, 'Invalid credentials');
    await expect(login('a@b.com', 'wrong')).rejects.toThrow('Invalid credentials');
  });
});
