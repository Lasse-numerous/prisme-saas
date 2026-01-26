/**
 * Detail view component for APIKey.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { APIKeyDetailBase, type APIKeyDetailBaseProps } from '../_generated/APIKeyDetailBase';

interface APIKeyDetailProps extends APIKeyDetailBaseProps {
  // Add your custom props here
}

/**
 * APIKey detail view component.
 *
 * Customize this component to add:
 * - Related data sections
 * - Custom formatting
 * - Actions
 */
export function APIKeyDetail(props: APIKeyDetailProps): JSX.Element {
  return (
    <div className="api-key-detail-container">
      <APIKeyDetailBase {...props} />
      {/* Add related data, custom sections here */}
    </div>
  );
}

export default APIKeyDetail;
