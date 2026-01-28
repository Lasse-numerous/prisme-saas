/**
 * Detail page for AllowedEmailDomain.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAllowedEmailDomain, useAllowedEmailDomainMutations } from '../../hooks/useAllowedEmailDomain';
import { AllowedEmailDomainDetail } from '../../components/allowed-email-domain/AllowedEmailDomainDetail';

export default function AllowedEmailDomainDetailPage(): JSX.Element {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { data, loading, error } = useAllowedEmailDomain(id ? parseInt(id, 10) : null);
  const { remove, loading: deleting } = useAllowedEmailDomainMutations();

  const handleBack = () => {
    navigate('/allowed-email-domains');
  };

  const handleEdit = () => {
    navigate(`/allowed-email-domains/${id}/edit`);
  };

  const handleDelete = async () => {
    if (!id) return;
    if (window.confirm('Are you sure you want to delete this allowedemaildomain?')) {
      const success = await remove(parseInt(id, 10));
      if (success) {
        navigate('/allowed-email-domains');
      }
    }
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

  if (loading || !data) {
    return (
      <div className="page-container">
        <div className="card p-12 flex items-center justify-center">
          <div className="animate-pulse flex items-center gap-3">
            <div className="w-2 h-2 bg-muted rounded-full animate-bounce" />
            <div className="w-2 h-2 bg-muted rounded-full animate-bounce [animation-delay:0.1s]" />
            <div className="w-2 h-2 bg-muted rounded-full animate-bounce [animation-delay:0.2s]" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <AllowedEmailDomainDetail
        data={data}
        loading={deleting}
        onBack={handleBack}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </div>
  );
}
