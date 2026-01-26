/**
 * Form component for Subdomain.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { SubdomainFormBase, type SubdomainFormBaseProps } from '../_generated/SubdomainFormBase';
import { WidgetProvider } from '../../prism/widgets';

// Import custom widgets if needed
// import { CustomEmailWidget } from '../widgets/CustomEmailWidget';

interface SubdomainFormProps extends SubdomainFormBaseProps {
  // Add your custom props here
}

/**
 * Subdomain form component.
 *
 * Customize this component to add:
 * - Custom widget overrides
 * - Additional form fields
 * - Custom validation
 * - Side effects
 */
export function SubdomainForm(props: SubdomainFormProps): JSX.Element {
  return (
    <WidgetProvider
      widgets={{
        // Override widgets for this form
        // 'Subdomain.email': CustomEmailWidget,
      }}
    >
      <div className="subdomain-form-wrapper">
        <SubdomainFormBase {...props} />
        {/* Add custom content here */}
      </div>
    </WidgetProvider>
  );
}

export default SubdomainForm;
