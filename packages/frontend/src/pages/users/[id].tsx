/**
 * Detail page for User.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useUser, useUserMutations } from '../../hooks/useUser';
import { UserDetail } from '../../components/user/UserDetail';

export default function UserDetailPage(): JSX.Element {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { data, loading, error } = useUser(id ? parseInt(id, 10) : null);
  const { remove, loading: deleting } = useUserMutations();

  const handleBack = () => {
    navigate('/users');
  };

  const handleEdit = () => {
    navigate(`/users/${id}/edit`);
  };

  const handleDelete = async () => {
    if (!id) return;
    if (window.confirm('Are you sure you want to delete this user?')) {
      const success = await remove(parseInt(id, 10));
      if (success) {
        navigate('/users');
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
      <UserDetail
        data={data}
        loading={deleting}
        onBack={handleBack}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </div>
  );
}
