# CHANGELOG


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
