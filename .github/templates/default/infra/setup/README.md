# Setup Modules

This folder contains optional infrastructure setup modules and configurations.

## Purpose

The `setup/` folder is for infrastructure components that are:
- **Optional** — Not required for basic operations
- **One-time** — Set up once, rarely changed
- **Foundational** — Enable other features

## Future Modules

Planned modules for this folder:

### OIDC (OpenID Connect)

Enable GitHub Actions to assume AWS roles for deployment.

- **Purpose**: Secure credential management
- **Status**: Not yet implemented
- **When needed**: If deploying to AWS

### Other Setup Modules

Additional infrastructure setup components will be added here as needed:
- Security configurations
- Authentication/authorization setup
- Infrastructure prerequisites
- Third-party integrations

## Usage

When a module is ready in this folder:

1. Create `infra/setup/[module-name]/` directory
2. Add Terraform files
3. Document in this README
4. Update main `infra/default/main.tf` to reference if needed

## Current Status

✗ Empty — No setup modules currently configured

See `infra/default/README.md` for main infrastructure configuration.
