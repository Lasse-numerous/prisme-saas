/**
 * Edit page for Subdomain.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useSubdomain, useSubdomainMutations } from '../../../hooks/useSubdomain';
import { SubdomainForm } from '../../../components/subdomain/SubdomainForm';
import type { SubdomainCreate } from '../../../types/generated';

export default function SubdomainEditPage(): JSX.Element {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { data, loading: fetching, error: fetchError } = useSubdomain(
    id ? parseInt(id, 10) : null
  );
  const { update, loading: updating, error: updateError } = useSubdomainMutations();

  const handleSubmit = async (formData: SubdomainCreate) => {
    if (!id) return;
    const result = await update(parseInt(id, 10), formData);
    if (result) {
      navigate(`/subdomains/${id}`);
    }
  };

  const handleCancel = () => {
    navigate(`/subdomains/${id}`);
  };

  const error = fetchError || updateError;

  if (fetching || !data) {
    return (
      <div className="page-container max-w-2xl">
        <div className="card p-12 flex items-center justify-center">
          <div className="animate-pulse flex items-center gap-3">
            <div className="w-2 h-2 bg-nordic-400 rounded-full animate-bounce" />
            <div className="w-2 h-2 bg-nordic-400 rounded-full animate-bounce [animation-delay:0.1s]" />
            <div className="w-2 h-2 bg-nordic-400 rounded-full animate-bounce [animation-delay:0.2s]" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container max-w-2xl">
      <header className="page-header">
        <h1 className="page-title">Edit Subdomain</h1>
        <p className="page-subtitle">Update subdomain details</p>
      </header>

      {error && (
        <div className="card p-4 mb-6 border-red-200 bg-red-50">
          <p className="text-red-700 text-sm">Error: {error.message}</p>
        </div>
      )}

      <div className="card p-6">
        <SubdomainForm
          onSubmit={handleSubmit}
          defaultValues={data}
          loading={updating}
          submitLabel="Save Changes"
          onCancel={handleCancel}
        />
      </div>
    </div>
  );
}
