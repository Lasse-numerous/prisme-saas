import { type ReactElement } from 'react';
import { Link } from 'react-router-dom';

export default function LandingPage(): ReactElement {
  return (
    <div className="page-container">
      {/* Hero */}
      <div className="card p-12 text-center mb-8">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
          </svg>
        </div>
        <h1 className="text-3xl font-bold text-foreground mb-3">
          Claim your <code className="text-primary">*.madewithpris.me</code> subdomain
        </h1>
        <p className="text-muted max-w-lg mx-auto mb-8">
          Get a free subdomain with instant DNS provisioning, automatic TLS, and
          flexible routing — all managed through a simple dashboard or API.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link to="/signup" className="btn btn-primary px-6 py-2.5">
            Get Started
          </Link>
          <Link to="/login" className="btn btn-secondary px-6 py-2.5">
            Sign In
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6">
          <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
            <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 className="font-semibold text-foreground mb-2">Instant DNS</h3>
          <p className="text-sm text-muted">
            Your subdomain is live in seconds with automatic A record creation via Hetzner DNS.
          </p>
        </div>

        <div className="card p-6">
          <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
            <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 className="font-semibold text-foreground mb-2">Custom Routing</h3>
          <p className="text-sm text-muted">
            Point your subdomain to any IP and port with Traefik-powered reverse proxy routing.
          </p>
        </div>

        <div className="card p-6">
          <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
            <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
          </div>
          <h3 className="font-semibold text-foreground mb-2">API Access</h3>
          <p className="text-sm text-muted">
            Manage subdomains programmatically with REST and GraphQL APIs plus API key authentication.
          </p>
        </div>
      </div>
    </div>
  );
}
