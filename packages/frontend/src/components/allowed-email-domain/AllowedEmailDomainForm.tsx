/**
 * Form component for AllowedEmailDomain.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { AllowedEmailDomainFormBase, type AllowedEmailDomainFormBaseProps } from '../_generated/AllowedEmailDomainFormBase';
import { WidgetProvider } from '../../prism/widgets';

// Import custom widgets if needed
// import { CustomEmailWidget } from '../widgets/CustomEmailWidget';

interface AllowedEmailDomainFormProps extends AllowedEmailDomainFormBaseProps {
  // Add your custom props here
}

/**
 * AllowedEmailDomain form component.
 *
 * Customize this component to add:
 * - Custom widget overrides
 * - Additional form fields
 * - Custom validation
 * - Side effects
 */
export function AllowedEmailDomainForm(props: AllowedEmailDomainFormProps): JSX.Element {
  return (
    <WidgetProvider
      widgets={{
        // Override widgets for this form
        // 'AllowedEmailDomain.email': CustomEmailWidget,
      }}
    >
      <div className="allowed-email-domain-form-wrapper">
        <AllowedEmailDomainFormBase {...props} />
        {/* Add custom content here */}
      </div>
    </WidgetProvider>
  );
}

export default AllowedEmailDomainForm;
