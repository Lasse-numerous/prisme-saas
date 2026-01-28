/**
 * Table component for AllowedEmailDomain.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { AllowedEmailDomainTableBase, type AllowedEmailDomainTableBaseProps } from '../_generated/AllowedEmailDomainTableBase';

interface AllowedEmailDomainTableProps extends AllowedEmailDomainTableBaseProps {
  // Add your custom props here
}

/**
 * AllowedEmailDomain table component.
 *
 * Customize this component to add:
 * - Custom column rendering
 * - Additional columns
 * - Toolbar actions
 * - Filters
 */
export function AllowedEmailDomainTable(props: AllowedEmailDomainTableProps): JSX.Element {
  return (
    <div className="allowed-email-domain-table-container">
      {/* Add custom toolbar here */}
      <AllowedEmailDomainTableBase {...props} />
      {/* Add custom footer here */}
    </div>
  );
}

export default AllowedEmailDomainTable;
