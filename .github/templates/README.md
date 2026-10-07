# Repository Templates

This directory contains versioned templates for new repositories created by the provisioning system.

## Template Structure

```
.github/templates/
├── README.md            (This file)
├── default/             (Default template)
│   ├── TEMPLATE_README.md
│   ├── .github/
│   ├── apps/
│   ├── conf/
│   ├── infra/
│   ├── Jenkinsfile
│   ├── config.yml
│   ├── prisma-cloud-config.yml
│   └── README.md
└── repo-scaffold/       (Scaffolding template - used by bootstrap scripts)
    ├── .github/
    ├── apps/
    ├── infra/
    └── ...
```

## Available Templates

### `default/` — Default Template

The standard template for new repositories. Includes:

- **Workflows**: CI/CD with GitHub Actions and Jenkins
- **Infrastructure**: Terraform scaffolding in `infra/default/`
- **Documentation**: `conf/ARCHITECTURE.md` and `conf/CONTRIBUTING.md`
- **Configuration**: Security scanning, repository config
- **Applications**: App manifest scaffolding

**Usage**: When creating a new repository, this template is automatically applied.

### `repo-scaffold/` — Scaffolding Template

Special template used by the `bootstrap_repo.py` script. Used for:

- Initial repository setup
- File copying and customization
- Metadata generation

## Creating a New Template

To create a new template variant (e.g., `enterprise/`, `minimal/`, `advanced/`):

1. Create new folder: `.github/templates/new-template/`
2. Copy structure from `default/` as base
3. Customize files for specific use case
4. Add `TEMPLATE_README.md` explaining the template
5. Update provisioning system to reference new template

Example:
```
.github/templates/
├── default/              # Standard template
├── enterprise/           # Enterprise-specific template
└── minimal/             # Lightweight template
```

## Updating Templates

When updating template files:

1. Make changes in the template folder
2. Commit changes to the provisioning repo
3. New repositories created afterward will use updated template
4. Existing repositories are not affected by template updates

## Template Best Practices

### 1. Include Documentation

Every template should include:
- `TEMPLATE_README.md` — How to use the template
- `conf/ARCHITECTURE.md` — System design overview
- `conf/CONTRIBUTING.md` — Contribution guidelines
- `README.md` — Project template and placeholders

### 2. Consistent Structure

Maintain consistent folder structure across templates:
- `.github/workflows/` — CI/CD workflows
- `apps/` — Application code
- `infra/default/` — Infrastructure code
- `conf/` — Documentation

### 3. Placeholder Content

Use `[TODO]` placeholders in templates for fields that should be customized:
- Project descriptions
- Team information
- Environment settings
- Links and references

### 4. Version Naming

Use clear names for template versions:
- `default` — Standard/current template
- `enterprise` — Enterprise-specific features
- `minimal` — Lightweight version
- `advanced` — Advanced/experimental features
- `legacy` — Previous version (deprecated)

### 5. Document Changes

When creating new templates, document:
- Purpose and use cases
- What's different from `default/`
- Migration path (if replacing another template)
- Support status

## Template Usage in Provisioning

When a new repository is created with a specified template:

```hcl
"my-repo" = {
  description = "Repository description"
  repository_template = "default"  # Uses .github/templates/default/
}
```

The provisioning system:
1. Creates the repository on GitHub
2. Clones the template from this repo
3. Applies template files to the new repo
4. Commits initial files
5. Creates initial PR (if configured)

## Future Templates

Potential templates for future use:

- **`enterprise/`** — Enterprise-grade with advanced security and compliance
- **`minimal/`** — Lightweight template for simple projects
- **`data-science/`** — Python, Jupyter, MLOps focused
- **`api/`** — REST/GraphQL API template
- **`infrastructure/`** — Specialized for infrastructure-as-code projects

## Support

For template questions or issues:
- See `TEMPLATE_README.md` in specific template
- Check provisioning repo documentation
- Contact the platform/devops team
