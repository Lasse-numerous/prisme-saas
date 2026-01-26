/**
 * Table component for Subdomain.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { SubdomainTableBase, type SubdomainTableBaseProps } from '../_generated/SubdomainTableBase';

interface SubdomainTableProps extends SubdomainTableBaseProps {
  // Add your custom props here
}

/**
 * Subdomain table component.
 *
 * Customize this component to add:
 * - Custom column rendering
 * - Additional columns
 * - Toolbar actions
 * - Filters
 */
export function SubdomainTable(props: SubdomainTableProps): JSX.Element {
  return (
    <div className="subdomain-table-container">
      {/* Add custom toolbar here */}
      <SubdomainTableBase {...props} />
      {/* Add custom footer here */}
    </div>
  );
}

export default SubdomainTable;
