/**
 * Detail view component for User.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { UserDetailBase, type UserDetailBaseProps } from '../_generated/UserDetailBase';

interface UserDetailProps extends UserDetailBaseProps {
  // Add your custom props here
}

/**
 * User detail view component.
 *
 * Customize this component to add:
 * - Related data sections
 * - Custom formatting
 * - Actions
 */
export function UserDetail(props: UserDetailProps): JSX.Element {
  return (
    <div className="user-detail-container">
      <UserDetailBase {...props} />
      {/* Add related data, custom sections here */}
    </div>
  );
}

export default UserDetail;
