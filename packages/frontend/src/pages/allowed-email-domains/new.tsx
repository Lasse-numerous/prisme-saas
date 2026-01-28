/**
 * Create page for AllowedEmailDomain.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAllowedEmailDomainMutations } from '../../hooks/useAllowedEmailDomain';
import { AllowedEmailDomainForm } from '../../components/allowed-email-domain/AllowedEmailDomainForm';
import type { AllowedEmailDomainCreate } from '../../types/generated';

export default function AllowedEmailDomainCreatePage(): JSX.Element {
  const navigate = useNavigate();
  const { create, loading, error } = useAllowedEmailDomainMutations();

  const handleSubmit = async (data: AllowedEmailDomainCreate) => {
    const result = await create(data);
    if (result) {
      navigate(`/allowed-email-domains/${result.id}`);
    }
  };

  const handleCancel = () => {
    navigate('/allowed-email-domains');
  };

  return (
    <div className="page-container max-w-2xl">
      <header className="page-header">
        <h1 className="page-title">Create AllowedEmailDomain</h1>
        <p className="page-subtitle">Add a new allowedemaildomain to your collection</p>
      </header>

      {error && (
        <div className="card p-4 mb-6 border-red-200 bg-red-50">
          <p className="text-red-700 text-sm">Error: {error.message}</p>
        </div>
      )}

      <div className="card p-6">
        <AllowedEmailDomainForm
          onSubmit={handleSubmit}
          loading={loading}
          submitLabel="Create"
          onCancel={handleCancel}
        />
      </div>
    </div>
  );
}
