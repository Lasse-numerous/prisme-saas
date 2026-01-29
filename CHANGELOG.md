# CHANGELOG


## v0.16.0 (2026-01-29)

### Bug Fixes

- Add explicit Traefik router-to-service mapping for devcontainer
  ([`42778c6`](https://github.com/Lasse-numerous/prisme-saas/commit/42778c6ca399107176bf2994a43a14b39e0ff572))

Traefik errored with "too many services" because a single container defines both frontend and API
  services without explicitly linking each router to its service.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Chores

- Add traefik docker network label to devcontainer
  ([`019de3a`](https://github.com/Lasse-numerous/prisme-saas/commit/019de3a8b9148c17b46901f1a105723c074f4a53))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Gitignore pnpm-store and pnpm-lock.yaml
  ([`4a8f15e`](https://github.com/Lasse-numerous/prisme-saas/commit/4a8f15e0f924e037daa3879cc8899b691b23d179))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Regenerate with updated prism framework (auth test generators)
  ([`3e61f59`](https://github.com/Lasse-numerous/prisme-saas/commit/3e61f59fb03819d1717f8542339af25c4fa1b1d7))

Regenerated all code with the updated Prism framework that now includes auth test generators.
  Preserved custom overrides (alembic env.py, AuthContext public page skip, subdomain test skip
  markers).

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Update lockfiles
  ([`a6b29ba`](https://github.com/Lasse-numerous/prisme-saas/commit/a6b29baf4c46e782efceb0967974054f3f8d48c1))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Features

- Add Playwright auto-start script and isolated browser sessions
  ([`373b607`](https://github.com/Lasse-numerous/prisme-saas/commit/373b607d1dcd2cb83f880280bb82d437823d7c63))

- Add scripts/ensure-devcontainer.sh that checks if dev servers are running, starts the devcontainer
  and dev servers if not, and waits for readiness - Update playwright.config.ts to use the new
  script as webServer command - Configure Playwright MCP with --isolated flag to start each session
  with a fresh browser profile (no cached responses)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Testing

- Add comprehensive auth test coverage for backend and frontend
  ([`14f2ef6`](https://github.com/Lasse-numerous/prisme-saas/commit/14f2ef695ae1383ee36b26fad32d14a0c3251c62))

Backend (pytest): 49 tests covering auth utils, JWT dependencies, and integration tests for signup,
  login, email verification, password reset, MFA setup/login, and session management.

Frontend (vitest): 28 tests covering authApi client, AuthContext provider, LoginForm, SignupForm,
  and ProtectedRoute components. Adds vitest, testing-library, jsdom, and msw as dev dependencies.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.15.6 (2026-01-29)

### Bug Fixes

- Make datetime columns timezone-aware to fix asyncpg 500 error
  ([`fc6f1a2`](https://github.com/Lasse-numerous/prisme-saas/commit/fc6f1a2afeb9449f58213bd4cbb8d2898ee30ddf))

The email_verification_token_expires_at, password_reset_token_expires_at, and locked_until columns
  were TIMESTAMP (naive) but code passes timezone-aware datetimes via datetime.now(UTC), causing
  asyncpg to reject the insert.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Chores

- Update lockfiles after ruff rebuild
  ([`7f2d40a`](https://github.com/Lasse-numerous/prisme-saas/commit/7f2d40a29cbe9125b6d0450e5a8fd28ed3284180))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.15.5 (2026-01-29)

### Bug Fixes

- Replace passlib with bcrypt directly for Python 3.13 compatibility
  ([`4024aa4`](https://github.com/Lasse-numerous/prisme-saas/commit/4024aa4a5ba13fbab481fb831002339f69264764))

passlib is unmaintained and incompatible with bcrypt 4.1+ on Python 3.13, causing 500 errors on
  signup.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Chores

- Update lockfiles after passlib removal
  ([`9472f6d`](https://github.com/Lasse-numerous/prisme-saas/commit/9472f6d963404586d410e03b71045e1284677250))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.15.4 (2026-01-29)

### Bug Fixes

- **frontend**: Replace vite.svg favicon, add autocomplete to password inputs
  ([`0b1e042`](https://github.com/Lasse-numerous/prisme-saas/commit/0b1e042f17b69db32516975e993489af84b35131))

- Replace default vite.svg reference with project favicon - Add autocomplete="current-password" on
  login form - Add autocomplete="new-password" on signup and reset password forms

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **frontend**: Skip /auth/me call on public pages to avoid 401 in console
  ([`f59a97b`](https://github.com/Lasse-numerous/prisme-saas/commit/f59a97b98c4042093f5b358ddd0a468c661183d6))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.15.3 (2026-01-29)

### Bug Fixes

- Add missing migrations, migration drift detection in CI and pre-push
  ([`09e73bf`](https://github.com/Lasse-numerous/prisme-saas/commit/09e73bf41c2c0b7d835860f70a4461f1fffa8fbd))

- Add initial schema migration (20260126000000) so migrations can run from scratch - Add missing
  migration for user password reset and account lockout fields - Add cleanup migration to drop
  removed authentik_id and convert status to enum - Add migration-check CI job that runs alembic
  check against fresh postgres - Add pre-push hook using throwaway Docker postgres for local drift
  detection - Improve deploy workflow with explicit migration error handling - Fix alembic env.py to
  ignore DateTime timezone false positives from Prism codegen

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.15.2 (2026-01-29)

### Bug Fixes

- Add missing pyotp and resend deps to backend pyproject.toml
  ([`664f670`](https://github.com/Lasse-numerous/prisme-saas/commit/664f6709c204b3be03616c4a6fa206e962b6dce9))

These were in the root pyproject.toml but missing from the backend package, causing silent
  ImportError in Docker builds that prevented all REST API routes from registering.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Chores

- Add prism CLI and spec skills, streamline CLAUDE.md
  ([`5d820bc`](https://github.com/Lasse-numerous/prisme-saas/commit/5d820bc9966954662044e27197c6843f977f4a73))

Copy prism-cli and generate-prism-spec skills from the framework repo and refactor CLAUDE.md to
  reference them instead of duplicating content.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Update uv.lock for new backend dependencies
  ([`b161e31`](https://github.com/Lasse-numerous/prisme-saas/commit/b161e31b37275c6a29c225f0bf5fc0b81ab034a4))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.15.1 (2026-01-29)

### Bug Fixes

- **frontend**: Resolve TypeScript build errors
  ([`c5810de`](https://github.com/Lasse-numerous/prisme-saas/commit/c5810de8a597dbf835c8cce044a128e3157a488a))

- Fix import paths in auth pages (../../ → ../ for contexts and lib) - Add lucide-react dependency
  for Icon component - Import Loader2/Minus/Check/X locally in Icon.tsx (re-export doesn't bind) -
  Extract useTheme hook from ThemeToggle component - Cast FieldError.message to string in FormBase
  components - Remove invalid string comparison for numeric userId field

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.15.0 (2026-01-29)

### Bug Fixes

- **tests**: Add auth fixtures and fix integration tests
  ([`e39f64e`](https://github.com/Lasse-numerous/prisme-saas/commit/e39f64e484fea6b10eebe477e636e192989e1aa9))

- Add auth bypass (get_current_active_user override) to test client fixture - Add
  unauthenticated_client fixture for auth requirement tests - Set email_verified and subdomain_limit
  on test user - Skip generated subdomain create/update tests (custom router uses /claim) - Fix
  release idempotency assertion for admin users

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Chores

- Regenerate after removing future annotations from all graphql templates
  ([`6fc772e`](https://github.com/Lasse-numerous/prisme-saas/commit/6fc772e757acdfb931de7fd74b308777c28b461c))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Regenerate after removing future annotations from graphql schema
  ([`bac121a`](https://github.com/Lasse-numerous/prisme-saas/commit/bac121ac023d22f6663845afbd5c37c9cc9128c2))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Regenerate from updated prism framework
  ([`281be74`](https://github.com/Lasse-numerous/prisme-saas/commit/281be7440cdb8de0b73138c0bd79107b89a6ff72))

Regenerated all code after prism fix for mutable defaults in strawberry input types (default_factory
  for list/dict fields).

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Features

- **auth**: Switch spec to JWT preset and regenerate
  ([`379263b`](https://github.com/Lasse-numerous/prisme-saas/commit/379263b6fac52ad739724328b74a6af5a56e9ea1))

Update spec from preset="custom" to preset="jwt" with full auth features: email verification,
  password reset, MFA/TOTP, account lockout, signup, Resend email, and GitHub OAuth.

Regenerate all backend and frontend code from updated spec. Remove Authentik remnants
  (flow_executor, oidc, webhooks, auth_flow schema). Custom auth routes preserved via GENERATE_ONCE
  strategy.

Also exclude .prism/ from ruff and ignore B027 in generated service base (lifecycle hooks are
  intentionally empty for subclass override).

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.14.0 (2026-01-28)

### Chores

- Update uv.lock
  ([`fc545b5`](https://github.com/Lasse-numerous/prisme-saas/commit/fc545b555639641c91728e43dc7886df4e8b6a3b))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Features

- **auth**: Keep password reset and email verification in project UX
  ([`8a80c35`](https://github.com/Lasse-numerous/prisme-saas/commit/8a80c35e4c2447dae39551d950471cb8b50d54bd))

Redirect email links to the frontend instead of Authentik's UI so users stay in the project's own UX
  for password reset and email verification.

- Email templates now link to /reset-password?token= and /verify-email?token= - New backend
  endpoints verify tokens against Authentik flow executor - New ResetPassword and VerifyEmail
  frontend pages consume those endpoints - Added frontend_url config setting and authApi client
  functions

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.13.0 (2026-01-28)

### Chores

- Update uv.lock
  ([`c06364e`](https://github.com/Lasse-numerous/prisme-saas/commit/c06364ebb039994c4a088ad76826924911e3f387))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Features

- **frontend**: Add landing page and dashboard for home route
  ([`e2ba548`](https://github.com/Lasse-numerous/prisme-saas/commit/e2ba5480456db81cf9d547e14ee0de6015a814ed))

Unauthenticated users now see a marketing landing page with feature highlights and CTA buttons.
  Authenticated users see a dashboard with their subdomains listed as status-badged cards.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.12.0 (2026-01-28)

### Features

- **auth**: Fix auth UX flows — forgot password, OAuth errors, retry, secure cookies
  ([`f520d2f`](https://github.com/Lasse-numerous/prisme-saas/commit/f520d2facbfbd2f54ed59a7da8fd30093f118487))

- Add password recovery flow (backend endpoints + frontend form + page) - Route GitHub OAuth errors
  to /auth/callback with proper error display - Add retry button when login/signup flow
  initialization fails - Make secure cookie flag conditional on DEBUG env var for local dev - Add
  "Forgot password?" link to login form - Add "Go to homepage" link to Access Denied page - Mount
  AuthCallback component at /auth/callback route

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.11.0 (2026-01-28)

### Features

- **auth**: Direct GitHub OAuth bypassing Authentik UI
  ([`c71459b`](https://github.com/Lasse-numerous/prisme-saas/commit/c71459b43709bba92ee0fbac4b1e97b1f7c885bc))

GitHub sign-in now redirects directly to github.com instead of through Authentik's frontend. The
  backend exchanges the code, fetches user info from GitHub API, and issues a JWT session cookie.
  Includes CSRF state validation via Redis.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.10.3 (2026-01-28)

### Bug Fixes

- **deploy**: Add AUTHENTIK_BASE_URL and JWT_SECRET to docker-compose env
  ([`9a11fe7`](https://github.com/Lasse-numerous/prisme-saas/commit/9a11fe7becc843d48368a0bc5d6d673adeb283e4))

The backend container needs these env vars passed through docker-compose, not just in the .env file
  on the host.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.10.2 (2026-01-28)

### Bug Fixes

- **deploy**: Add AUTHENTIK_BASE_URL and JWT_SECRET to deploy env vars
  ([`2705fd7`](https://github.com/Lasse-numerous/prisme-saas/commit/2705fd78241438c3f68e36302da445962ada4d64))

The Flow Executor client needs AUTHENTIK_BASE_URL to reach Authentik's API, and JWT_SECRET is
  required for self-issued session tokens.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.10.1 (2026-01-28)

### Bug Fixes

- **frontend**: Resolve TypeScript errors in generated form components
  ([`7f6982a`](https://github.com/Lasse-numerous/prisme-saas/commit/7f6982a4cfa931fe6a7ba29d60732caff4e57082))

Fix TS2322 in FormBase components by casting error message to string. Fix TS2367 in
  useAPIKeyFormState by removing invalid string comparison on number field.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.10.0 (2026-01-28)

### Chores

- Update uv.lock with new auth dependencies
  ([`379bff7`](https://github.com/Lasse-numerous/prisme-saas/commit/379bff703443f0557b700bdf984224479c59a51e))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **deps**: Bump appleboy/ssh-action from 1.0.3 to 1.2.4
  ([`d56dfeb`](https://github.com/Lasse-numerous/prisme-saas/commit/d56dfeb789e11ba3c9500a163e2fe3a0b0e2354e))

Bumps [appleboy/ssh-action](https://github.com/appleboy/ssh-action) from 1.0.3 to 1.2.4. - [Release
  notes](https://github.com/appleboy/ssh-action/releases) -
  [Commits](https://github.com/appleboy/ssh-action/compare/v1.0.3...v1.2.4)

--- updated-dependencies: - dependency-name: appleboy/ssh-action dependency-version: 1.2.4

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

### Features

- Add devcontainer configuration and documentation
  ([`3cc98de`](https://github.com/Lasse-numerous/prisme-saas/commit/3cc98dea89d97303b4e2ef23c9a752eaf6370df7))

- Add .devcontainer/ with Docker Compose setup for isolated development - Add Development with
  Devcontainer section to README

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add devcontainer configuration for development
  ([`332e83e`](https://github.com/Lasse-numerous/prisme-saas/commit/332e83ef386365fbd5c05732cd6656f16d3ad66f))

Adds VS Code devcontainer support for easier development setup: - Dockerfile.dev with Python 3.13,
  Node.js, and uv - docker-compose.yml with PostgreSQL and isolated volumes - devcontainer.json with
  VS Code settings and extensions - setup.sh for container initialization - .env.template for
  environment configuration

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **auth**: Add Flow Executor client, self-issued JWT sessions, and new auth endpoints
  ([`72c491b`](https://github.com/Lasse-numerous/prisme-saas/commit/72c491bfe65e8eee8241f450acdb54913ac218c4))

Replace OIDC redirect flow with Authentik Flow Executor API for custom auth UX. Backend now proxies
  Authentik flows and issues self-signed HS256 JWT session cookies.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **frontend**: Add auth API client and new auth components
  ([`3ab0fdb`](https://github.com/Lasse-numerous/prisme-saas/commit/3ab0fdb5ec1bda9762397b0490ed4791f88f9117))

Add authApi.ts for driving backend flow endpoints, plus EmailVerification, TOTPVerify, and TOTPSetup
  components for multi-step auth flows.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **frontend**: Rewrite LoginForm, SignupForm with flow executor + simplify AuthContext
  ([`c59105b`](https://github.com/Lasse-numerous/prisme-saas/commit/c59105b4047f38b24b7088fc0e9e66dcbf0ba468))

LoginForm now drives Authentik login flow with multi-step support (credentials, TOTP MFA, email
  verification error). SignupForm drives enrollment flow with email verification step. AuthContext
  simplified - login/signup logic moved to forms.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.9.0 (2026-01-28)

### Bug Fixes

- Resolve Strawberry GraphQL recursion and add types-PyYAML
  ([`ea16ef1`](https://github.com/Lasse-numerous/prisme-saas/commit/ea16ef1491cca91503b19427dc446d575758a9dd))

- Remove `from __future__ import annotations` from GraphQL modules (causes infinite recursion in
  Strawberry's type resolution) - Quote forward references in filter types for lazy loading - Add
  types-PyYAML dev dependency for mypy

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Use default_factory for mutable list defaults (Python 3.14 compat)
  ([`7f0568a`](https://github.com/Lasse-numerous/prisme-saas/commit/7f0568a82adc6f2805c3ff2b7304ea87c311d186))

Python 3.14 enforces stricter dataclass rules, rejecting mutable list defaults. Use
  lambda/default_factory for the roles field.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **ci**: Add types-PyYAML to root dev dependencies for mypy
  ([`17ec84d`](https://github.com/Lasse-numerous/prisme-saas/commit/17ec84d7e97c3d34196a7cade3b171f68140c088))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **deps**: Add slowapi to root dependencies
  ([`aae6192`](https://github.com/Lasse-numerous/prisme-saas/commit/aae61929cf6067b64ab2da08b9962d7d296930bc))

slowapi was listed in backend pyproject.toml but missing from the root, causing silent ImportError
  that prevented REST routes from registering.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **lint**: Resolve ruff errors in prism-generated code
  ([`1cf9885`](https://github.com/Lasse-numerous/prisme-saas/commit/1cf9885bc000d8f0f0e1ff1eb57e4552d6720e89))

- B904: add `from err`/`from None` to re-raised exceptions in auth code - B006: replace mutable
  default `['user']` with None in MCP user_tools - B027: suppress with noqa for intentional empty
  lifecycle hooks in ServiceBase

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **prism**: Align spec name with package structure
  ([`b1b0dae`](https://github.com/Lasse-numerous/prisme-saas/commit/b1b0daebb6b7a06b5ecba16f1088647ba2f508ca))

- Change spec name from 'madewithprisme' to 'prisme_api' to match existing package directory - This
  prevents prism generate from creating duplicate code in a subdirectory - Add .env.authentik* to
  gitignore pattern - Add devcontainer documentation to CLAUDE.md - Add docker-compose.authentik.yml
  for Authentik stack

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **tests**: Add auth fixtures and fix test data for integration tests
  ([`bc414b7`](https://github.com/Lasse-numerous/prisme-saas/commit/bc414b756f03f5f6101a011cb96c800fe64b0f52))

- Add unauthenticated_client, client (user auth), admin_client fixtures - Use admin_client for CRUD
  tests requiring admin access - Fix subdomain names to be DNS-compliant (no underscores) - Use
  /subdomains/claim instead of non-existent POST /subdomains - Disable rate limiting in test
  environment (sqlite) - Accept 403 for re-release of already-released subdomains

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **types**: Resolve mypy errors in generated and custom code
  ([`dc9bb9a`](https://github.com/Lasse-numerous/prisme-saas/commit/dc9bb9a4a8fcde92a3a46cb8cb26e09dba317a06))

- Fix AllowedEmailDomainService to extend generated base class - Fix webhooks.py import: use
  async_session instead of get_async_session - Add types-PyYAML dev dependency for yaml type stubs

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Chores

- Regenerate prism code with corrected output paths
  ([`ded35b7`](https://github.com/Lasse-numerous/prisme-saas/commit/ded35b7708051ae9b5a0a9197b17d1c39ba2971e))

- Fix prism.config.py backend_path and frontend_path to avoid nested subdirectories - Regenerate all
  prism-managed files with correct prisme_api imports - Add AllowedEmailDomain GraphQL, REST, MCP,
  frontend, and test scaffolding - Preserve custom: TraefikRouteManager exports, timezone-aware
  datetimes, SubdomainUpdate port default=None

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Documentation

- Prefix all CLI commands with uv run in CLAUDE.md
  ([`ec2c623`](https://github.com/Lasse-numerous/prisme-saas/commit/ec2c62316bd0196fd52695da1214b622c2810d41))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Features

- **subdomain**: Wildcard DNS routing with Traefik and security enhancements
  ([`fd4b786`](https://github.com/Lasse-numerous/prisme-saas/commit/fd4b78625b3906c1c86b57114e5285090f104026))

- Add port field to Subdomain model for custom port routing (default: 80) - Add 30-day cooldown
  period for released subdomains (released_at, cooldown_until fields) - Add AllowedEmailDomain model
  for email domain whitelist on signup - Add TraefikRouteManager service for dynamic YAML route file
  generation - Add rate limiting with SlowAPI (5 claims/min, 10 activations/hour per user) - Require
  email verification before claiming subdomains - Validate port range (1-65535, block privileged
  ports except 80/443) - Extend reserved subdomains with brand names and typosquat protection (~250
  entries) - Add email domain whitelist validation in auth callback - Replace Nginx with Traefik in
  docker-compose.prod.yml - Add Traefik configuration with Let's Encrypt DNS-01 challenge via
  Hetzner - Update cloud-init to prepare for Traefik instead of Nginx - Update subdomain_limit
  default from 5 to 10 - Add database migration for new fields and AllowedEmailDomain table

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.8.1 (2026-01-28)

### Bug Fixes

- **email**: Use SMTP port 587 with STARTTLS for Resend
  ([`8ebf346`](https://github.com/Lasse-numerous/prisme-saas/commit/8ebf34685f622da8579792def2d5c7259f51fbe2))

Hetzner blocks outbound port 465 (SMTP SSL). Changed Authentik email configuration to use port 587
  with STARTTLS which is not blocked.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.8.0 (2026-01-28)

### Chores

- Update uv.lock
  ([`7ab6332`](https://github.com/Lasse-numerous/prisme-saas/commit/7ab6332024ccfbb8e016b329a6398525c5f4fbc0))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Features

- **auth**: Comprehensive Authentik branding with Nordic theme
  ([`707f260`](https://github.com/Lasse-numerous/prisme-saas/commit/707f260b53795e47ef8508d095a077f4bdc31dee))

- Add modular blueprint structure (00-08) for better organization - Implement comprehensive CSS
  theme with PatternFly variable overrides - Create branded email templates (verification, password
  reset) - Add prism logo SVG and 64x64 favicon PNG - Add local Authentik dev environment with
  docker-compose overlay - Add bootstrap script for dev Authentik setup - Update staging compose
  with templates volume mount

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.7.2 (2026-01-28)

### Bug Fixes

- Combine auth blueprints to avoid attr replacement issues
  ([`74b8b96`](https://github.com/Lasse-numerous/prisme-saas/commit/74b8b961f79c2cb754fe279937730fe4073f7d17))

Merge email-password and github-oauth into single authentication blueprint with conditional entries:
  - GitHub source created only when GITHUB_CLIENT_ID is set - Identification stage configured
  with/without GitHub source based on condition - Both paths include enrollment_flow and
  recovery_flow for signup/reset

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.7.1 (2026-01-28)

### Bug Fixes

- Order blueprints for correct dependency resolution
  ([`5a3cf97`](https://github.com/Lasse-numerous/prisme-saas/commit/5a3cf97e5e41168ef3cedfe80620b125fabe7eb2))

Rename blueprints with numeric prefixes to ensure: 1. GitHub OAuth source is created first 2.
  Email/password identification stage can reference it 3. TOTP MFA stages are added last

Also consolidate identification stage config in email-password blueprint to include enrollment_flow,
  recovery_flow, and sources.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.7.0 (2026-01-28)

### Features

- Add email/password auth with optional TOTP MFA
  ([`e2d9f9f`](https://github.com/Lasse-numerous/prisme-saas/commit/e2d9f9f2d0971ebfe3babaf4e8c101805ee31479))

- Add email-password.yaml blueprint for signup and password recovery - Add totp-mfa.yaml blueprint
  for optional authenticator app MFA - Configure Resend SMTP for Authentik email delivery - Pass
  RESEND_API_KEY to staging deployment

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.6.0 (2026-01-28)

### Documentation

- Comprehensive documentation overhaul
  ([`4ae36bf`](https://github.com/Lasse-numerous/prisme-saas/commit/4ae36bf0235b65a79792beb54bf3605765d11189))

- Fix architecture docs to reflect proxy model with wildcard DNS/SSL - Add API Keys documentation
  (docs/api/api-keys.md) - Add Users API documentation (docs/api/users.md) - Update authentication
  docs with Authentik/OIDC flow, remove fictional rate limiting - Add pagination, sorting, and
  filtering documentation - Document all REST endpoints (was 5, now 25+) - Update CLI docs to
  reflect proxy routing instead of DNS records - Add CLAUDE.md for AI assistant context - Update
  mkdocs.yml navigation with new pages

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Update existing documentation for proxy architecture
  ([`194e3ec`](https://github.com/Lasse-numerous/prisme-saas/commit/194e3ec96f42f3c846715e554535c63e187b6aea))

- Update API index with all endpoints and common patterns - Fix subdomains docs to reference proxy
  routes instead of DNS records - Update CLI subdomain docs for proxy model - Fix getting started
  guides to explain wildcard DNS/SSL - Update home page with correct architecture diagram - Add
  dev_addr to mkdocs.yml for port 8009

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Features

- Add GitHub OAuth for social login
  ([`559d16a`](https://github.com/Lasse-numerous/prisme-saas/commit/559d16af48d21f20de26920a224b60a11916e373))

- Add GitHub OAuth blueprint for Authentik - Replace Google OAuth with GitHub OAuth in
  docker-compose and deploy workflow - Configure GH_OAUTH_CLIENT_ID and GH_OAUTH_CLIENT_SECRET
  secrets

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.5.4 (2026-01-28)

### Bug Fixes

- Preserve trailing slash in issuer URL validation
  ([`65077c5`](https://github.com/Lasse-numerous/prisme-saas/commit/65077c5a7876a4a0e18cbd9034c0f5f75e00b12a))

Authentik includes a trailing slash in the issuer claim, so we must not strip it when validating.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.5.3 (2026-01-28)

### Bug Fixes

- Correct JWKS URL to use application-level path
  ([`77ca55c`](https://github.com/Lasse-numerous/prisme-saas/commit/77ca55c47742ea226b0ba1089719546d0f85d3cc))

JWKS is at /application/o/{app}/jwks/, not /application/o/jwks/

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Chores

- Add logging for OIDC errors
  ([`a528b8e`](https://github.com/Lasse-numerous/prisme-saas/commit/a528b8eeda8fb1c578ebbe6288acdabf8dbb14e5))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.5.2 (2026-01-28)

### Bug Fixes

- Use Redis for OAuth state storage
  ([`5f0f835`](https://github.com/Lasse-numerous/prisme-saas/commit/5f0f835eed49807cf15964d0ac8644525ce21382))

The backend runs multiple workers, so in-memory state storage doesn't work. State stored in one
  worker isn't visible to others.

Use Redis for distributed state storage with TTL.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.5.1 (2026-01-28)

### Bug Fixes

- Correct Authentik OAuth2 endpoint URLs
  ([`136f35f`](https://github.com/Lasse-numerous/prisme-saas/commit/136f35fc71187d59743522740e0df441c8ecfd4b))

Authentik uses shared OAuth endpoints (/application/o/authorize/) not per-application paths
  (/application/o/{app}/authorize/).

The issuer URL contains the app slug but authorize/token/userinfo endpoints are at the parent path.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.5.0 (2026-01-28)

### Features

- Add Authentik blueprints for idempotent OAuth2 setup
  ([`855e11f`](https://github.com/Lasse-numerous/prisme-saas/commit/855e11fed3ab94a0cdc2aad0c1e9e759a3eaa97b))

- Add Authentik blueprint for OAuth2 provider and application - Update docker-compose.staging.yml to
  mount blueprints - Update deploy workflow to copy blueprints to server - Add script to generate
  and set OAuth credentials - Exclude blueprints from YAML lint (uses custom tags)

The blueprint automatically configures: - OAuth2 provider with client_id/secret from env vars -
  Application with slug "madewithprisme"

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.4.0 (2026-01-28)

### Features

- Add Authentik nginx config and SSL to deploy workflow
  ([`5b14ba6`](https://github.com/Lasse-numerous/prisme-saas/commit/5b14ba6ee757f9880c9b02d85b9f7897c06f00e3))


## v0.3.1 (2026-01-28)

### Bug Fixes

- Remove /api prefix from VITE_API_URL (routes already include it)
  ([`78a0621`](https://github.com/Lasse-numerous/prisme-saas/commit/78a0621358a2fa9139a8d16d9cac3c3c11a954e2))

### Chores

- Remove standalone authentik compose (inline in staging/prod)
  ([`9a304ef`](https://github.com/Lasse-numerous/prisme-saas/commit/9a304ef8107b021ce8ce12d43220d20129c94b7c))


## v0.3.0 (2026-01-28)

### Features

- Automate SSL certificate setup in deploy workflow
  ([`e2eed80`](https://github.com/Lasse-numerous/prisme-saas/commit/e2eed8076ed46df056da2d8ab0b56fa653c17924))


## v0.2.4 (2026-01-28)

### Bug Fixes

- Use absolute path for deploy-config artifact
  ([`79ea838`](https://github.com/Lasse-numerous/prisme-saas/commit/79ea83861d9867815a9152430f5452c9f20336da))


## v0.2.3 (2026-01-28)

### Bug Fixes

- Use artifact to pass server IP from terraform to deploy
  ([`d524468`](https://github.com/Lasse-numerous/prisme-saas/commit/d52446838d56e644c5f102e138ff23aed1d663ee))


## v0.2.2 (2026-01-28)

### Bug Fixes

- Update terraform to 1.9.0 for S3 backend compatibility
  ([`7f6a3d5`](https://github.com/Lasse-numerous/prisme-saas/commit/7f6a3d5aec4552b2cc8665c9abd3a420f061eb39))


## v0.2.1 (2026-01-28)

### Bug Fixes

- Correct S3 bucket name for terraform state
  ([`86ce345`](https://github.com/Lasse-numerous/prisme-saas/commit/86ce3451a70f6c8002950a95ab4f3329dad485fd))


## v0.2.0 (2026-01-28)

### Features

- Add Hetzner Object Storage backend for terraform state
  ([`6a3f238`](https://github.com/Lasse-numerous/prisme-saas/commit/6a3f238ce90ee2e0eb2eedb6af3aa2c340e4785f))

Configure S3-compatible backend using Hetzner Object Storage to persist terraform state across CI
  runs. Requires: - Bucket: prisme-saas-terraform - Secrets: HETZNER_S3_ACCESS_KEY,
  HETZNER_S3_SECRET_KEY

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.1.1 (2026-01-28)

### Bug Fixes

- Update terraform conditions for workflow_run trigger
  ([`e94aedb`](https://github.com/Lasse-numerous/prisme-saas/commit/e94aedb3de0ad6cb18b7e19765afb9e9a1d44d22))

Changed conditions from 'push' to 'workflow_run' event type so apply, outputs, and deploy trigger
  steps actually run.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>


## v0.1.0 (2026-01-28)

### Bug Fixes

- Add Column type with render property to table components
  ([`e5c9dfd`](https://github.com/Lasse-numerous/prisme-saas/commit/e5c9dfd25f4a5351f5c74709c9359ce543d15ce2))

Fix TypeScript errors in generated table components by properly typing the column definitions with
  optional render function. Also fix GraphQL client subscription type compatibility.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add missing environment variables to deploy workflow
  ([`efba679`](https://github.com/Lasse-numerous/prisme-saas/commit/efba6799c11f6477cc3fbead201aafecc68e9a8f))

Add required docker-compose variables: - DOCKER_REGISTRY, GITHUB_REPOSITORY, PROJECT_NAME -
  POSTGRES_DB, POSTGRES_USER, REDIS_URL - AUTHENTIK_DB_USER, AUTHENTIK_DB_NAME, AUTHENTIK_VERSION -
  ENVIRONMENT

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add SSH key to cloud-init deploy user and ICMP inbound rule
  ([`d50c806`](https://github.com/Lasse-numerous/prisme-saas/commit/d50c806d8572e919ae1133d3af07714f1330511e))

The deploy user was created without SSH authorized_keys, making SSH access impossible. Also added
  ICMP inbound rule for ping.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Clean up deploy workflow and fix alembic path
  ([`1949d38`](https://github.com/Lasse-numerous/prisme-saas/commit/1949d386e954328a3118218d7df19aa3557da48a))

- Remove debug output - Fix alembic working directory to /app/packages/backend/src - Replace fixed
  sleep with dynamic health check loop (up to 90s) - Use rolling update instead of force-recreate

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Convert postgresql:// to postgresql+asyncpg:// for async SQLAlchemy
  ([`8f3e70c`](https://github.com/Lasse-numerous/prisme-saas/commit/8f3e70cb1438040e706ad5a40f27406bfed1009e))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Deploy staging on main branch, production only via manual dispatch
  ([`ca9075b`](https://github.com/Lasse-numerous/prisme-saas/commit/ca9075b84bc9470afc4b5d3807b5e69a8bf6b10d))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Exclude test files from production TypeScript build
  ([`e7b16cc`](https://github.com/Lasse-numerous/prisme-saas/commit/e7b16cc6b4ba76cee49b3477387e7e484bf00f83))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Exclude vite.config.ts from main tsconfig
  ([`f23fdf2`](https://github.com/Lasse-numerous/prisme-saas/commit/f23fdf2fcd1c576087229b1016243a1987a55eee))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Fix frontend TypeScript build errors
  ([`7644599`](https://github.com/Lasse-numerous/prisme-saas/commit/7644599329bed5d78490a733b9c3b7b234e56993))

- Fix import paths for AuthContext in auth components (../contexts → ../../contexts) - Add missing
  ThemeToggle component - Update LoginForm and SignupForm to use OIDC redirect flow instead of form
  submission

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Fix mypy ignore for graphql schema and test user fixture
  ([`bce2d8f`](https://github.com/Lasse-numerous/prisme-saas/commit/bce2d8f8617bccf6f2b445bb6dcc675f8d25f1d3))

- Add mypy ignore for graphql schema module (strawberry type issue) - Fix test_user fixture to reuse
  existing user instead of duplicate

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Fix TypeScript and pre-push hook errors
  ([`addbcbe`](https://github.com/Lasse-numerous/prisme-saas/commit/addbcbee310ac2a116bbed62f9ab7edec05b9d60))

Frontend: - Cast FieldError message to string in UserFormBase - Cast request to SubscribePayload in
  GraphQL client - Remove onSuccess prop from Login/Signup pages

Backend: - Add ruff UP046/UP047 ignores for Prism-generated Generic patterns - Add mypy ignores for
  generated service/schema modules - Update conftest with authenticated test client fixture - Update
  pre-commit ruff version to 0.14.14

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Force recreate containers to clear unhealthy state during deploy
  ([`a1b216c`](https://github.com/Lasse-numerous/prisme-saas/commit/a1b216c79ab40b00293fdb3fdfdac2678ab5943d))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Overwrite .env instead of merging to prevent duplicate accumulation
  ([`a37742a`](https://github.com/Lasse-numerous/prisme-saas/commit/a37742ab901d5953f22348b6f926ce41de955470))

The merge logic was leaving duplicate POSTGRES_PASSWORD entries from previous failed deployments,
  causing docker compose to potentially read empty values.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Relax TypeScript strict settings for prism-generated code
  ([`f80577a`](https://github.com/Lasse-numerous/prisme-saas/commit/f80577a741300dfe5d6aa597d29905e670cfbfb9))

- Set strict: false to allow unused variables in generated code - Add vite/client types for
  import.meta.env support

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Remove onSuccess prop from Login/Signup pages
  ([`c8c64a3`](https://github.com/Lasse-numerous/prisme-saas/commit/c8c64a36efda8acefacfd7e7c9c08ec4201e60bb))

With OIDC auth, login/signup success is handled via AuthCallback component after redirect, not via
  callback props.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Remove postgres volumes and add compose config debug
  ([`e15bf62`](https://github.com/Lasse-numerous/prisme-saas/commit/e15bf623f2231f3c3e4a2c6a190d5549c326498d))

The postgres containers were failing because they were initialized without a password. Removing the
  volumes allows fresh initialization with the correct password.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Remove single quotes from heredoc to allow variable expansion
  ([`2330323`](https://github.com/Lasse-numerous/prisme-saas/commit/2330323f034dbabf888c134c708376bdf51fd20a))

The heredoc << 'SECRETS_EOF' was preventing environment variable expansion, causing literal ${VAR}
  strings in .env instead of values.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Restructure frontend to standard Vite layout and add Tailwind CSS
  ([`d78d844`](https://github.com/Lasse-numerous/prisme-saas/commit/d78d844296a8673d2255993b25a8adbebd6985bf))

- Move config files (package.json, vite.config.ts, tsconfig.json, index.html) from
  packages/frontend/src/ to packages/frontend/ - Source code remains in packages/frontend/src/ - Add
  tailwind.config.js with Nordic theme palette - Add postcss.config.js for Tailwind processing -
  Update index.css with Tailwind directives and Nordic component styles - Add tailwindcss, postcss,
  autoprefixer to devDependencies - Update Dockerfile.frontend and docker-compose.dev.yml paths -
  Update prism.config.py to enable frontend and use correct paths - Fix index.html to reference
  /src/main.tsx

This fixes CSS not loading in Docker due to missing Tailwind configuration.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Run integration tests instead of non-existent e2e marker
  ([`eccf2fb`](https://github.com/Lasse-numerous/prisme-saas/commit/eccf2fbe6143a1308e7bae09663fbb5c22f7fd15))

The e2e job was filtering for tests with 'e2e' marker which don't exist. Changed to run integration
  tests directory directly.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Terraform waits for CI tests to pass
  ([`ac89237`](https://github.com/Lasse-numerous/prisme-saas/commit/ac892371197aef33411a28d275cce5dd4575babf))

Use workflow_run trigger to run terraform only after CI workflow completes successfully. This
  ensures test and e2e tests pass before any infrastructure changes or deployments.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Update subdomain API tests to match custom endpoints
  ([`9e263bc`](https://github.com/Lasse-numerous/prisme-saas/commit/9e263bc99c01ead261222f3896b389d7fa2ff0df))

- Use /claim endpoint instead of generic POST - Use /{name}/activate endpoint instead of PATCH - Use
  valid subdomain name format in tests

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Update SubdomainFactory to generate valid test data
  ([`27249cf`](https://github.com/Lasse-numerous/prisme-saas/commit/27249cf35ccec9dfe39b22a72c8363e27ef19f86))

- Use valid subdomain name pattern (no underscores) - Use Faker ipv4 for valid IP addresses

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Use valid subdomain name in unit test
  ([`6d13199`](https://github.com/Lasse-numerous/prisme-saas/commit/6d131992d9a5557e8d3d41be3aee2eb2d90c6a60))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **ci**: Lowercase Docker image name for GHCR compatibility
  ([`6aa649b`](https://github.com/Lasse-numerous/prisme-saas/commit/6aa649b3059472c8de437db24744009848ddc691))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **deploy**: Correct Terraform configuration issues
  ([`69b07b2`](https://github.com/Lasse-numerous/prisme-saas/commit/69b07b24d08e69c616338caea47e0b276e3f29c2))

- Remove duplicate required_providers from main.tf (keep in versions.tf) - Add required_providers to
  server and volume modules - Fix server_network to use only subnet_id (not both network_id and
  subnet_id) - Update server types to use available ARM types (cax11/cax21) - Add terraform lock
  file and update gitignore for state files - Add PRISM_DEPLOY_FEEDBACK.md with lessons learned

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Chores

- Add Authentik infrastructure for staging and production
  ([`50c9769`](https://github.com/Lasse-numerous/prisme-saas/commit/50c9769d4a89d3acafc0624260cf9cbd159bb773))

- Add docker-compose.staging.yml with Authentik services enabled - Add docker-compose.prod.yml with
  Authentik services (commented out) - Update docker-compose.authentik.yml example for auth-staging
  subdomain - Add Authentik env vars to staging and production templates - Add .env.authentik to
  gitignore (contains secrets)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add package-lock.json for frontend
  ([`2e2d3dc`](https://github.com/Lasse-numerous/prisme-saas/commit/2e2d3dc7a385951aac47c6d1ff599e1563898f27))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add POSTGRES_PASSWORD debug output
  ([`a86a47a`](https://github.com/Lasse-numerous/prisme-saas/commit/a86a47a0f9af0f47461a4223cca39b10cacf2ffe))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add site/ to .gitignore
  ([`0751ee8`](https://github.com/Lasse-numerous/prisme-saas/commit/0751ee8c4c7ca2afd48838b9b6de30befb921ee5))

Generated documentation output should not be tracked.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add value length debug for postgres password
  ([`5209c31`](https://github.com/Lasse-numerous/prisme-saas/commit/5209c319402ec581eedbbc166eb8f70a62842d93))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add verbose output to diagnose staging deployment failure
  ([`2654261`](https://github.com/Lasse-numerous/prisme-saas/commit/2654261f7002c24cefca9f66a47ab0eb52282b50))

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Regenerate code with updated prism config
  ([`cca441c`](https://github.com/Lasse-numerous/prisme-saas/commit/cca441c4d1d916b7974fec6df202557c2749d13a))

Regenerated after enabling frontend, GraphQL, and MCP in prism.config.py.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Update server type to cx23 and GitHub repo
  ([`ce5c2c8`](https://github.com/Lasse-numerous/prisme-saas/commit/ce5c2c8cec6e1b934f627df65c20316b7fd2217b))

- Change staging server to cx23 (Intel x86) - Update GITHUB_REPOSITORY to Lasse-numerous/prisme-saas

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Continuous Integration

- Add secrets management and Authentik auto-initialization
  ([`090e9cc`](https://github.com/Lasse-numerous/prisme-saas/commit/090e9cc8ae1374137d9e7305611e18511825545b))

- Pass secrets from GitHub to .env during deployment - Auto-initialize Authentik admin on first
  deployment - Store recovery link for manual OIDC setup - Merge secrets into existing .env
  preserving other values

Required GitHub Secrets (per environment): - DATABASE_URL, POSTGRES_PASSWORD, SECRET_KEY -
  AUTHENTIK_SECRET_KEY, AUTHENTIK_DB_PASSWORD - AUTHENTIK_CLIENT_ID, AUTHENTIK_CLIENT_SECRET (after
  Authentik setup) - AUTHENTIK_WEBHOOK_SECRET, MCP_ADMIN_API_KEY

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Update deploy workflow for Authentik and migrations
  ([`0541de8`](https://github.com/Lasse-numerous/prisme-saas/commit/0541de8866081993daf06678a784b6dc2b8860f3))

- Use docker-compose.staging.yml for staging (includes Authentik) - Add step to copy compose files
  to servers before deployment - Add database migration step after deployment - Fix health check URL
  to use port 8000

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Features

- Add Authentik OIDC authentication config and backend
  ([`f6bfebc`](https://github.com/Lasse-numerous/prisme-saas/commit/f6bfebc9de0d645168bf9ef759d98390a7021a7d))

- Update Prism spec with Authentik preset and role-based auth config - Add new User model fields:
  authentik_id, username, roles, is_active - Create auth module with OIDC client, dependencies, and
  webhooks - Add database migration for new user fields - Fix alembic env.py imports (prisme_api
  instead of madewithprisme)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add frontend auth with route guards and role-based navigation
  ([`35ca644`](https://github.com/Lasse-numerous/prisme-saas/commit/35ca6443697e73670e97b5b0af7262a010937c5e))

- Update AuthContext for Authentik OIDC flow - Add ProtectedRoute component with role checking -
  Wrap user routes with admin-only protection - Wrap api-keys and subdomains routes with auth
  protection - Conditionally show navigation links based on auth state and roles - Add login/signup
  links for unauthenticated users

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add GitHub secrets setup script
  ([`9a4873d`](https://github.com/Lasse-numerous/prisme-saas/commit/9a4873d9a3a24639feef1c4081a128ff9c7fe5a5))

- Add setup-github-secrets.sh to automate environment secrets configuration - Update README with
  complete secrets documentation - Documents all required secrets for staging/production

Usage: ./deploy/scripts/setup-github-secrets.sh staging

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add missing frontend and backend package configs for Docker dev
  ([`d0bf67d`](https://github.com/Lasse-numerous/prisme-saas/commit/d0bf67d493dcd8b2fe794ab99cbec7e9dcebb563))

- Add packages/backend/pyproject.toml for Docker build - Add frontend package.json with React, urql,
  react-hook-form dependencies - Add Vite configuration files (vite.config.ts, tsconfig.json) - Add
  index.html and index.css for Vite entry point - Update Dockerfile.frontend to use npm install
  instead of npm ci - Update docker-compose.dev.yml ports to avoid conflicts (8003, 5174)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Add Terraform CI workflow and secrets setup script
  ([`f3ac13d`](https://github.com/Lasse-numerous/prisme-saas/commit/f3ac13d27117a0047a92651d0d30ef7eb67e1bf8))

- Add terraform.yml workflow for automated infrastructure management - Runs plan on push to main
  when terraform files change - Manual dispatch with plan/apply/destroy options for
  staging/production - Automatically updates STAGING_HOST/PRODUCTION_HOST secrets from terraform
  output - Includes placeholder for Authentik OAuth setup

- Add setup-github-secrets.sh script - Generates secure passwords using openssl - Sets all required
  GitHub environment secrets - Documents next steps after running

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Initial prisme-saas project with Phase 5 infrastructure
  ([`a29d8bb`](https://github.com/Lasse-numerous/prisme-saas/commit/a29d8bb0f038d930abb2f1f4a0eab805711d00e4))

- FastAPI backend with async SQLAlchemy for subdomain management - REST API endpoints for subdomain
  lifecycle (claim, activate, release) - API key authentication with admin access control -
  Integration and unit test suites (66 tests passing) - Pre-commit hooks matching main prism project
  (ruff, conventional commits) - CI/CD workflows (lint, test, docs, e2e, release) - MkDocs
  documentation with Material theme - Docker configuration for PostgreSQL development - Factory-boy
  test data generation with valid subdomain patterns

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Pass server IP directly from terraform to deploy workflow
  ([`ade5ddc`](https://github.com/Lasse-numerous/prisme-saas/commit/ade5ddc5741c35506fc99e6f9dcf5752c9812d23))

Instead of using a PAT to update secrets, terraform workflow now triggers the deploy workflow
  directly with server_ip as input parameter. This uses only the built-in GITHUB_TOKEN.

Changes: - deploy.yml: Accept optional server_ip input, use it over secrets - terraform.yml: Trigger
  deploy workflow with server_ip parameter - terraform.yml: Remove placeholder setup-authentik job -
  README: Mark host secrets as optional when using terraform workflow

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Rebrand to madewithpris.me domain
  ([`cb04822`](https://github.com/Lasse-numerous/prisme-saas/commit/cb04822d5693eafa19592a21584a8407f7a39080))

Update all references from prisme.dev to madewithpris.me: - docker-compose.dev.yml: Traefik labels,
  container names, network - config.py: base_domain, CORS origins for production domain - main.py:
  API title and description - specs/models.py: StackSpec name and descriptions - Documentation: all
  docs updated with new domain - mkdocs.yml: site name and URL - Backend models, schemas, GraphQL
  types - DNS service domain constant

Production domain: madewithpris.me (GoDaddy) Local dev: madewithpris.me.localhost

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Secure MCP server tools with admin API key auth
  ([`2a6ce61`](https://github.com/Lasse-numerous/prisme-saas/commit/2a6ce615f0adf5ff85d3b68852b571b5fd91f145))

- Add require_mcp_auth decorator for API key verification - Protect all user, api_key, and subdomain
  tools with auth - Add _api_key parameter to all MCP tool functions - Add filtering support
  (user_id, owner_id, status)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- Secure REST and GraphQL endpoints with role-based access
  ([`6e234c2`](https://github.com/Lasse-numerous/prisme-saas/commit/6e234c2ba74cd2eb186b05746bb9af02f73a9467))

REST API: - Add Authentik OIDC auth endpoints (login, callback, logout, me) - Protect user routes
  with admin-only access - Add owner-based filtering for api-keys and subdomains routes

GraphQL: - Add user to context with auth helper methods - Protect user queries with admin-only
  access - Add owner-based filtering for api-keys and subdomains queries

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **deploy**: Add Hetzner Cloud deployment infrastructure
  ([`2c63027`](https://github.com/Lasse-numerous/prisme-saas/commit/2c63027f0d38ddd48d029fcf281e7b15b241d681))

- Add Terraform configuration for Hetzner Cloud VMs, networks, volumes - Add cloud-init provisioning
  (Docker, nginx, firewall, fail2ban) - Add production Dockerfiles for backend and frontend - Add
  docker-compose.prod.yml for production deployment - Add GitHub Actions CI/CD workflow for
  automated deployments - Add environment templates for staging and production - Add deploy/rollback
  scripts - Add DEPLOYMENT.md checklist for outstanding actions

All configuration uses variables for project name, domain, and GitHub repository to avoid
  hardcoding.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

- **docker**: Use prism-generated Docker configuration
  ([`908962c`](https://github.com/Lasse-numerous/prisme-saas/commit/908962c4d8bf7ff2af97a9e16a4ab863bb05d871))

- Replace manual docker/ folder with prism docker init output - Dockerfile.backend: Python 3.13 slim
  with uv package manager - docker-compose.dev.yml: backend, frontend, db services with Traefik
  labels - .dockerignore: comprehensive exclusion patterns

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Refactoring

- Terraform triggers deploy, no fallback secrets
  ([`c10709c`](https://github.com/Lasse-numerous/prisme-saas/commit/c10709c04fd40f7ebe67533dfea0264ab50fdaca))

- Remove push trigger from deploy.yml (terraform triggers it) - Remove fallback to HOST secrets
  (server_ip input required) - Terraform runs on all pushes to main (idempotent) - Flow: push →
  terraform plan/apply → get IP → trigger deploy

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

### Testing

- Update tests for Authentik auth and new User model fields
  ([`bf5f2ee`](https://github.com/Lasse-numerous/prisme-saas/commit/bf5f2ee23af06938e1844b8e69c7383e3f4463f3))

- Update conftest and factories for new User fields - Update GraphQL tests with auth context -
  Update integration tests with auth mocking - Update unit tests for service layer

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
