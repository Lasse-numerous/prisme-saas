/**
 * Auth API client for driving Authentik flows through the backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export interface FlowChallenge {
  type: string;
  title?: string | null;
  fields?: Array<{
    name: string;
    label: string;
    type: string;
    required: boolean;
    placeholder?: string;
  }> | null;
  sources?: Array<{ name: string; icon_url: string }> | null;
  password_fields?: boolean | null;
  totp_url?: string | null;
  error?: string | null;
}

export interface FlowStartResponse {
  flow_token: string;
  challenge: FlowChallenge;
}

export interface FlowStepResponse {
  challenge?: FlowChallenge | null;
  completed: boolean;
  user?: Record<string, unknown> | null;
  error?: string | null;
  redirect_to?: string | null;
}

async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || `Request failed: ${response.status}`);
  }

  return response.json();
}

export async function startLoginFlow(): Promise<FlowStartResponse> {
  return apiPost('/api/auth/flow/login/start', {});
}

export async function submitLoginFlow(
  flowToken: string,
  data: Record<string, unknown>
): Promise<FlowStepResponse> {
  return apiPost('/api/auth/flow/login/submit', {
    flow_token: flowToken,
    data,
  });
}

export async function startSignupFlow(): Promise<FlowStartResponse> {
  return apiPost('/api/auth/flow/signup/start', {});
}

export async function submitSignupFlow(
  flowToken: string,
  data: Record<string, unknown>
): Promise<FlowStepResponse> {
  return apiPost('/api/auth/flow/signup/submit', {
    flow_token: flowToken,
    data,
  });
}

export async function resendVerificationEmail(
  flowToken: string
): Promise<void> {
  await apiPost('/api/auth/flow/signup/resend-email', {
    flow_token: flowToken,
    data: {},
  });
}

export async function startRecoveryFlow(): Promise<FlowStartResponse> {
  return apiPost('/api/auth/flow/recovery/start', {});
}

export async function submitRecoveryFlow(
  flowToken: string,
  data: Record<string, unknown>
): Promise<FlowStepResponse> {
  return apiPost('/api/auth/flow/recovery/submit', {
    flow_token: flowToken,
    data,
  });
}

export function getGitHubLoginUrl(): string {
  return `${API_BASE_URL}/api/auth/github/login`;
}
