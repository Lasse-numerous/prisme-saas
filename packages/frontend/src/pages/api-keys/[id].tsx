/**
 * Detail page for APIKey.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAPIKey, useAPIKeyMutations } from '../../hooks/useAPIKey';
import { APIKeyDetail } from '../../components/api-key/APIKeyDetail';

export default function APIKeyDetailPage(): JSX.Element {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { data, loading, error } = useAPIKey(id ? parseInt(id, 10) : null);
  const { remove, loading: deleting } = useAPIKeyMutations();

  const handleBack = () => {
    navigate('/api-keys');
  };

  const handleEdit = () => {
    navigate(`/api-keys/${id}/edit`);
  };

  const handleDelete = async () => {
    if (!id) return;
    if (window.confirm('Are you sure you want to delete this apikey?')) {
      const success = await remove(parseInt(id, 10));
      if (success) {
        navigate('/api-keys');
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
      <APIKeyDetail
        data={data}
        loading={deleting}
        onBack={handleBack}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </div>
  );
}
