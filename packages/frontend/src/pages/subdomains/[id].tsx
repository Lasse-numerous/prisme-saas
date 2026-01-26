/**
 * Detail page for Subdomain.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useSubdomain, useSubdomainMutations } from '../../hooks/useSubdomain';
import { SubdomainDetail } from '../../components/subdomain/SubdomainDetail';

export default function SubdomainDetailPage(): JSX.Element {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { data, loading, error } = useSubdomain(id ? parseInt(id, 10) : null);
  const { remove, loading: deleting } = useSubdomainMutations();

  const handleBack = () => {
    navigate('/subdomains');
  };

  const handleEdit = () => {
    navigate(`/subdomains/${id}/edit`);
  };

  const handleDelete = async () => {
    if (!id) return;
    if (window.confirm('Are you sure you want to delete this subdomain?')) {
      const success = await remove(parseInt(id, 10));
      if (success) {
        navigate('/subdomains');
      }
    }
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

  if (loading || !data) {
    return (
      <div className="page-container">
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
    <div className="page-container">
      <SubdomainDetail
        data={data}
        loading={deleting}
        onBack={handleBack}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </div>
  );
}
