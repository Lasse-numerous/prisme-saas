/**
 * Form component for APIKey.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { APIKeyFormBase, type APIKeyFormBaseProps } from '../_generated/APIKeyFormBase';
import { WidgetProvider } from '../../prism/widgets';

// Import custom widgets if needed
// import { CustomEmailWidget } from '../widgets/CustomEmailWidget';

interface APIKeyFormProps extends APIKeyFormBaseProps {
  // Add your custom props here
}

/**
 * APIKey form component.
 *
 * Customize this component to add:
 * - Custom widget overrides
 * - Additional form fields
 * - Custom validation
 * - Side effects
 */
export function APIKeyForm(props: APIKeyFormProps): JSX.Element {
  return (
    <WidgetProvider
      widgets={{
        // Override widgets for this form
        // 'APIKey.email': CustomEmailWidget,
      }}
    >
      <div className="api-key-form-wrapper">
        <APIKeyFormBase {...props} />
        {/* Add custom content here */}
      </div>
    </WidgetProvider>
  );
}

export default APIKeyForm;
