/**
 * List page for Subdomains.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSubdomainList, useSubdomainMutations } from '../../hooks/useSubdomain';
import { SubdomainTable } from '../../components/subdomain/SubdomainTable';
import type { Subdomain } from '../../types/generated';

export default function SubdomainsListPage(): JSX.Element {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const { data, loading, error, totalCount, hasNextPage, hasPreviousPage, refetch } = useSubdomainList({
    page,
    pageSize: 20,
  });
  const { remove, loading: mutating } = useSubdomainMutations();

  const handleRowClick = (item: Subdomain) => {
    navigate(`/subdomains/${item.id}`);
  };

  const handleEdit = (item: Subdomain) => {
    navigate(`/subdomains/${item.id}/edit`);
  };

  const handleDelete = async (item: Subdomain) => {
    if (window.confirm('Are you sure you want to delete this subdomain?')) {
      await remove(item.id);
      refetch();
    }
  };

  const handleCreate = () => {
    navigate('/subdomains/new');
  };

  if (error) {
    return (
      <div className="page-container">
        <div className="card p-6 border-red-200 bg-red-50">
          <p className="text-red-700">Error: {error.message}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <header className="page-header flex items-center justify-between">
        <div>
          <h1 className="page-title">Subdomains</h1>
          <p className="page-subtitle">Manage your subdomains</p>
        </div>
        <button onClick={handleCreate} className="btn-primary">
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Create Subdomain
        </button>
      </header>

      <div className="card overflow-hidden">
        <SubdomainTable
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
        <p className="text-sm text-nordic-500">
          Page {page} · {totalCount} total
        </p>
      </div>
    </div>
  );
}
