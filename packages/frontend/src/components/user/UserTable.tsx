/**
 * Table component for User.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { UserTableBase, type UserTableBaseProps } from '../_generated/UserTableBase';

interface UserTableProps extends UserTableBaseProps {
  // Add your custom props here
}

/**
 * User table component.
 *
 * Customize this component to add:
 * - Custom column rendering
 * - Additional columns
 * - Toolbar actions
 * - Filters
 */
export function UserTable(props: UserTableProps): JSX.Element {
  return (
    <div className="user-table-container">
      {/* Add custom toolbar here */}
      <UserTableBase {...props} />
      {/* Add custom footer here */}
    </div>
  );
}

export default UserTable;
