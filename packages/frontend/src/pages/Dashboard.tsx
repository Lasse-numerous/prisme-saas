import { type ReactElement } from 'react';
import { Link } from 'react-router-dom';
import { useSubdomainList } from '../hooks/useSubdomain';

const STATUS_STYLES: Record<string, string> = {
  active: 'bg-green-100 text-green-800',
  reserved: 'bg-yellow-100 text-yellow-800',
  suspended: 'bg-red-100 text-red-800',
  released: 'bg-gray-100 text-gray-600',
};

export default function Dashboard(): ReactElement {
  const { data: subdomains, loading, error } = useSubdomainList({ page: 1, pageSize: 50 });

  return (
    <div className="page-container">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold text-foreground">My Subdomains</h1>
        <Link to="/subdomains/new" className="btn btn-primary">
          Claim New Subdomain
        </Link>
      </div>

      {/* Error */}
      {error && (
        <div className="card p-4 mb-6 border-red-300 bg-red-50 text-red-800 text-sm">
          Failed to load subdomains. Please try again later.
        </div>
      )}

      {/* Loading */}
      {loading && !subdomains.length && (
        <div className="card p-8 text-center text-muted">Loading...</div>
      )}

      {/* Empty state */}
      {!loading && !error && subdomains.length === 0 && (
        <div className="card p-8 text-center">
          <div className="w-16 h-16 bg-surface-sunken rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
          </div>
          <h2 className="text-lg font-semibold text-foreground mb-2">No subdomains yet</h2>
          <p className="text-muted mb-6">Claim your first <code>*.madewithpris.me</code> subdomain to get started.</p>
          <Link to="/subdomains/new" className="btn btn-primary">
            Claim Your First Subdomain
          </Link>
        </div>
      )}

      {/* Subdomain cards */}
      {subdomains.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {subdomains.map((sub) => (
            <Link
              key={sub.id}
              to={`/subdomains/${sub.id}`}
              className="card p-5 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-semibold text-foreground">
                  {(sub as any).name}.madewithpris.me
                </h3>
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${STATUS_STYLES[(sub as any).status] ?? 'bg-gray-100 text-gray-600'}`}>
                  {(sub as any).status}
                </span>
              </div>
              {(sub as any).ip_address && (
                <p className="text-xs text-muted">
                  IP: {(sub as any).ip_address}{(sub as any).port ? `:${(sub as any).port}` : ''}
                </p>
              )}
              <div className="mt-3 text-xs text-primary font-medium">
                View details &rarr;
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
