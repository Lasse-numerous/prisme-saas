/**
 * Form component for User.
 *
 * ✅ YOUR CODE - Safe to modify, will not be overwritten.
 * This file was generated once by Prism and is yours to customize.
 */

import React from 'react';
import { UserFormBase, type UserFormBaseProps } from '../_generated/UserFormBase';
import { WidgetProvider } from '../../prism/widgets';

// Import custom widgets if needed
// import { CustomEmailWidget } from '../widgets/CustomEmailWidget';

interface UserFormProps extends UserFormBaseProps {
  // Add your custom props here
}

/**
 * User form component.
 *
 * Customize this component to add:
 * - Custom widget overrides
 * - Additional form fields
 * - Custom validation
 * - Side effects
 */
export function UserForm(props: UserFormProps): JSX.Element {
  return (
    <WidgetProvider
      widgets={{
        // Override widgets for this form
        // 'User.email': CustomEmailWidget,
      }}
    >
      <div className="user-form-wrapper">
        <UserFormBase {...props} />
        {/* Add custom content here */}
      </div>
    </WidgetProvider>
  );
}

export default UserForm;
