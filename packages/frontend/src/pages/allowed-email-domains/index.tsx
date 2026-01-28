/**
 * List page for AllowedEmailDomains.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAllowedEmailDomainList, useAllowedEmailDomainMutations } from '../../hooks/useAllowedEmailDomain';
import { AllowedEmailDomainTable } from '../../components/allowed-email-domain/AllowedEmailDomainTable';
import type { AllowedEmailDomain } from '../../types/generated';

export default function AllowedEmailDomainsListPage(): JSX.Element {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const { data, loading, error, totalCount, hasNextPage, hasPreviousPage, refetch } = useAllowedEmailDomainList({
    page,
    pageSize: 20,
  });
  const { remove, loading: mutating } = useAllowedEmailDomainMutations();

  const handleRowClick = (item: AllowedEmailDomain) => {
    navigate(`/allowed-email-domains/${item.id}`);
  };

  const handleEdit = (item: AllowedEmailDomain) => {
    navigate(`/allowed-email-domains/${item.id}/edit`);
  };

  const handleDelete = async (item: AllowedEmailDomain) => {
    if (window.confirm('Are you sure you want to delete this allowedemaildomain?')) {
      await remove(item.id);
      refetch();
    }
  };

  const handleCreate = () => {
    navigate('/allowed-email-domains/new');
  };

  if (error) {
    return (
      <div className="page-container">
        <div className="alert-error">
          <p>Error: {error.message}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <header className="page-header flex items-center justify-between">
        <div>
          <h1 className="page-title">AllowedEmailDomains</h1>
          <p className="page-subtitle">Manage your allowedemaildomains</p>
        </div>
        <button onClick={handleCreate} className="btn-primary">
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Create AllowedEmailDomain
        </button>
      </header>

      <div className="card overflow-hidden">
        <AllowedEmailDomainTable
          data={data}
          loading={loading || mutating}
          onRowClick={handleRowClick}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </div>

      <div className="mt-6 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage((p) => p - 1)}
            disabled={!hasPreviousPage || loading}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <button
            onClick={() => setPage((p) => p + 1)}
            disabled={!hasNextPage || loading}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
        <p className="text-sm text-muted">
          Page {page} · {totalCount} total
        </p>
      </div>
    </div>
  );
}
