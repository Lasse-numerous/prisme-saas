/**
 * Table component for APIKey.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { APIKeyTableBase, type APIKeyTableBaseProps } from '../_generated/APIKeyTableBase';

interface APIKeyTableProps extends APIKeyTableBaseProps {
  // Add your custom props here
}

/**
 * APIKey table component.
 *
 * Customize this component to add:
 * - Custom column rendering
 * - Additional columns
 * - Toolbar actions
 * - Filters
 */
export function APIKeyTable(props: APIKeyTableProps): JSX.Element {
  return (
    <div className="api-key-table-container">
      {/* Add custom toolbar here */}
      <APIKeyTableBase {...props} />
      {/* Add custom footer here */}
    </div>
  );
}

export default APIKeyTable;
