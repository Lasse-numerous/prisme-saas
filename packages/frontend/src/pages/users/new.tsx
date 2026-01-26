/**
 * Create page for User.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useUserMutations } from '../../hooks/useUser';
import { UserForm } from '../../components/user/UserForm';
import type { UserCreate } from '../../types/generated';

export default function UserCreatePage(): JSX.Element {
  const navigate = useNavigate();
  const { create, loading, error } = useUserMutations();

  const handleSubmit = async (data: UserCreate) => {
    const result = await create(data);
    if (result) {
      navigate(`/users/${result.id}`);
    }
  };

  const handleCancel = () => {
    navigate('/users');
  };

  return (
    <div className="page-container max-w-2xl">
      <header className="page-header">
        <h1 className="page-title">Create User</h1>
        <p className="page-subtitle">Add a new user to your collection</p>
      </header>

      {error && (
        <div className="card p-4 mb-6 border-red-200 bg-red-50">
          <p className="text-red-700 text-sm">Error: {error.message}</p>
        </div>
      )}

      <div className="card p-6">
        <UserForm
          onSubmit={handleSubmit}
          loading={loading}
          submitLabel="Create"
          onCancel={handleCancel}
        />
      </div>
    </div>
  );
}
