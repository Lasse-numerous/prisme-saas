/**
 * Create page for Subdomain.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useSubdomainMutations } from '../../hooks/useSubdomain';
import { SubdomainForm } from '../../components/subdomain/SubdomainForm';
import type { SubdomainCreate } from '../../types/generated';

export default function SubdomainCreatePage(): JSX.Element {
  const navigate = useNavigate();
  const { create, loading, error } = useSubdomainMutations();

  const handleSubmit = async (data: SubdomainCreate) => {
    const result = await create(data);
    if (result) {
      navigate(`/subdomains/${result.id}`);
    }
  };

  const handleCancel = () => {
    navigate('/subdomains');
  };

  return (
    <div className="page-container max-w-2xl">
      <header className="page-header">
        <h1 className="page-title">Create Subdomain</h1>
        <p className="page-subtitle">Add a new subdomain to your collection</p>
      </header>

      {error && (
        <div className="card p-4 mb-6 border-red-200 bg-red-50">
          <p className="text-red-700 text-sm">Error: {error.message}</p>
        </div>
      )}

      <div className="card p-6">
        <SubdomainForm
          onSubmit={handleSubmit}
          loading={loading}
          submitLabel="Create"
          onCancel={handleCancel}
        />
      </div>
    </div>
  );
}
