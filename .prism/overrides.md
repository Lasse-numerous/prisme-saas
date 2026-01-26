# Code Override Log

**Last Updated**: 2026-01-26T17:05:43.545156

**Unreviewed Overrides**: 2


---


## ⚠️ packages/backend/src/prisme_api/api/rest/subdomain.py

**Strategy**: generate_once
**Status**: Not Reviewed
**Changes**: +0 lines, -0 lines, ~259 lines
**Last Modified**: 2026-01-26T17:05:43.545140

### What Changed

<details>
<summary>Show Diff</summary>

*Diff not available (run generation again to regenerate)*


</details>

### Actions

- Review your custom code to ensure it's still compatible
- Run `prism test` to verify functionality
- Run `prism review mark-reviewed packages/backend/src/prisme_api/api/rest/subdomain.py` when done

---


## ⚠️ packages/backend/src/prisme_api/services/subdomain.py

**Strategy**: generate_once
**Status**: Not Reviewed
**Changes**: +3 lines, -0 lines, ~20 lines
**Last Modified**: 2026-01-26T17:05:43.517851

### What Changed

<details>
<summary>Show Diff</summary>

```diff
--- generated+++ user@@ -1,32 +1,36 @@ """Service for Subdomain.

-✅ YOUR CODE - Safe to modify, will not be overwritten.
-This file was generated once by Prism and is yours to customize.
+Custom service logic for managing subdomains with Hetzner DNS integration.
 """

 from __future__ import annotations

+from sqlalchemy import select
+
 from ._generated.subdomain_base import SubdomainServiceBase
+from prisme_api.models.subdomain import Subdomain


 class SubdomainService(SubdomainServiceBase):
     """Custom service logic for Subdomain.

-    Add your custom methods and override base methods here.
+    Extends the base service with:
+    - Lookup by name (unique field)
+    - Subdomain validation
     """

-    # Example: Override a lifecycle hook
-    # async def before_create(self, data: SubdomainCreate) -> None:
-    #     # Custom validation or transformation
-    #     pass
+    async def get_by_name(self, name: str) -> Subdomain | None:
+        """Get a subdomain by its unique name.

-    # Example: Add a custom method
-    # async def find_by_email(self, email: str) -> Subdomain | None:
-    #     query = select(self.model).where(self.model.email == email)
-    #     result = await self.db.execute(query)
-    #     return result.scalar_one_or_none()
+        Args:
+            name: The subdomain name (e.g., 'myapp')

-    pass
+        Returns:
+            The Subdomain object if found, None otherwise
+        """
+        query = select(self.model).where(self.model.name == name.lower())
+        result = await self.db.execute(query)
+        return result.scalar_one_or_none()


 __all__ = ["SubdomainService"]

```

</details>

### Actions

- Review your custom code to ensure it's still compatible
- Run `prism test` to verify functionality
- Run `prism review mark-reviewed packages/backend/src/prisme_api/services/subdomain.py` when done

---
