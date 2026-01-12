# Skill Examples

This document contains comprehensive examples of different types of OpenCode skills, demonstrating various patterns, structures, and use cases.

## Table of Contents

1. [Analysis Skills](#analysis-skills)
2. [Generation Skills](#generation-skills) 
3. [Automation Skills](#automation-skills)
4. [Domain-Specific Skills](#domain-specific-skills)
5. [Multi-Modal Skills](#multi-modal-skills)

---

## Analysis Skills

### Code Analysis Example

**Skill:** `python-code-analyzer`

```yaml
---
name: python-code-analyzer
description: Analyze Python code for quality issues, security vulnerabilities, and performance problems. Use when you need comprehensive code review or want to identify potential issues in Python codebases.
license: MIT
scope: project
---
```

**Key Features:**
- Clear trigger conditions ("when you need comprehensive code review")
- Specific language focus
- Quality, security, and performance coverage

### Data Analysis Example

**Skill:** `data-insights`

```yaml
---
name: data-insights
description: Extract meaningful insights from datasets by analyzing patterns, trends, and anomalies. Use when you have raw data that needs interpretation or when you need to identify key trends and patterns for decision-making.
license: MIT
scope: global
---
```

**Key Features:**
- Domain-agnostic data focus
- Clear output expectations
- Global scope for general utility

---

## Generation Skills

### Code Generation Example

**Skill:** `api-client-generator`

```yaml
---
name: api-client-generator
description: Generate API client code from OpenAPI specifications. Use when you need to create client libraries for REST APIs or when you want to automate the process of creating API integration code.
license: MIT
scope: project
---
```

### Documentation Generation Example

**Skill:** `technical-documentation`

```yaml
---
name: technical-documentation
description: Create comprehensive technical documentation from code and specifications. Use when you need to generate API docs, user guides, or technical specifications from source code or requirements.
license: MIT
scope: global
---
```

---

## Automation Skills

### Build Automation Example

**Skill:** `build-orchestrator`

```yaml
---
name: build-orchestrator
description: Orchestrate complex build processes with multiple steps, dependencies, and error handling. Use when you need to automate multi-stage builds, handle build matrix configurations, or manage complex CI/CD pipelines.
license: MIT
scope: project
---
```

### Deployment Automation Example

**Skill:** `deployment-manager`

```yaml
---
name: deployment-manager
description: Manage application deployments with rollback capabilities and health checks. Use when you need to deploy applications safely, handle deployment configurations, or implement zero-downtime deployment strategies.
license: MIT
scope: project
---
```

---

## Domain-Specific Skills

### Security Analysis Example

**Skill:** `security-audit`

```yaml
---
name: security-audit
description: Conduct comprehensive security audits of code and infrastructure. Use when you need to identify security vulnerabilities, assess compliance with security standards, or implement security best practices.
license: MIT
scope: global
---
```

### Performance Optimization Example

**Skill:** `performance-tuner`

```yaml
---
name: performance-tuner
description: Optimize application performance through profiling and bottleneck analysis. Use when you need to improve application speed, reduce resource usage, or identify and resolve performance bottlenecks.
license: MIT
scope: project
---
```

---

## Multi-Modal Skills

### Document Processing Example

**Skill:** `document-processor`

```yaml
---
name: document-processor
description: Process and analyze multi-modal documents including PDFs, images, and structured data. Use when you need to extract information from complex documents, analyze visual content, or process mixed-format documentation.
license: MIT
scope: global
---
```

---

## Skill Pattern Examples

### Progressive Loading Pattern

**Basic SKILL.md** (under 500 lines):
```markdown
---
name: complex-processor
description: Process complex data with specialized analysis capabilities. Use when you need advanced data processing, custom analysis pipelines, or specialized transformation workflows.
license: MIT
scope: project
---
# Complex Processor

## What this skill does
Processes complex data through advanced analysis pipelines.

## When to use this skill
Use this when you need advanced data processing capabilities.

## Instructions
1. Analyze input data structure
2. Select appropriate processing pipeline
3. Execute transformation workflow
4. Generate formatted output

## Advanced Patterns
See [references/advanced-patterns.md](references/advanced-patterns.md) for complex processing strategies.

## Troubleshooting
Refer to [references/troubleshooting.md](references/troubleshooting.md) for common issues.
```

**Reference Content** (loaded on demand):
```markdown
# references/advanced-patterns.md

## Advanced Processing Strategies

### Pattern 1: Hierarchical Processing
- Handle nested data structures
- Implement recursive algorithms
- Optimize for large datasets

### Pattern 2: Parallel Processing
- Distribute workload across multiple workers
- Handle concurrent data streams
- Manage resource allocation

### Pattern 3: Streaming Processing
- Process data in chunks
- Handle real-time data feeds
- Implement backpressure handling
```

### Modular File Organization

**Directory Structure:**
```
complex-processor/
├── SKILL.md              # Core logic only
├── scripts/
│   ├── validate.py       # Skill validation
│   ├── processor.py      # Core processing logic
│   └── test.py          # Test suite
├── references/
│   ├── api-reference.md  # Detailed API docs
│   ├── examples.md      # Comprehensive examples
│   ├── patterns.md      # Processing patterns
│   └── troubleshooting.md
└── assets/
    ├── templates/       # Output templates
    ├── schemas/        # Data schemas
    └── configs/        # Default configurations
```

---

## Best Practice Examples

### Trigger Description Optimization

**Vague (Poor):**
```yaml
description: Analyzes code and provides feedback
```

**Specific (Good):**
```yaml
description: Analyze code for security vulnerabilities, performance issues, and maintainability problems. Use when you need comprehensive code review or want to identify potential issues before deployment.
```

### Scope Selection

**Project Scope (Project-Specific):**
```yaml
name: api-validator
description: Validate API endpoints against project-specific schema requirements. Use when you need to ensure API consistency within this project's architecture.
scope: project
```

**Global Scope (General Utility):**
```yaml
name: git-workflow
description: Manage Git workflows with common patterns and best practices. Use when you need to handle branch management, merge strategies, or version control operations across any project.
scope: global
```

### Progressive Content Organization

**Lean Main SKILL.md:**
```markdown
---
name: database-migrator
description: Manage database schema migrations with rollback capabilities. Use when you need to evolve database schemas safely or handle complex migration scenarios.
license: MIT
scope: project
---
# Database Migrator

## What this skill does
Manages safe database schema evolution and migrations.

## When to use this skill
Use this when you need to modify database structures or handle schema versioning.

## Instructions
1. Analyze current schema state
2. Generate migration scripts
3. Validate migration safety
4. Execute migration with rollback plan

## Migration Strategies
See [references/migration-patterns.md](references/migration-patterns.md) for detailed strategies.

## Database-Specific Patterns
Refer to [references/database-guides.md](references/database-guides.md) for your database system.
```

**Detailed Reference Content:**
```markdown
# references/migration-patterns.md

## Migration Strategies

### Strategy 1: Blue-Green Deployment
- Maintain two identical database environments
- Switch traffic seamlessly
- Immediate rollback capability

### Strategy 2: Shadow Schema
- Deploy changes alongside existing schema
- Gradual data migration
- Minimal downtime approach

### Strategy 3: Backwards Compatible Changes
- Always maintain compatibility
- Use feature flags for new functionality
- Plan for deprecation cycles
```

---

## Anti-Examples to Avoid

### Poor Trigger Description

```yaml
# BAD: Too generic, no clear trigger
description: This skill helps with processing tasks.

# BAD: Missing trigger conditions
description: Generates code from specifications.

# BAD: Too vague
description: Provides analysis and insights.
```

### Poor Skills Structure

```
# BAD: Monolithic file (2000+ lines)
skill-name/
└── SKILL.md              # Contains everything
```

```
# BAD: Inconsistent structure
skill-name/
├── skill.md              # Wrong filename
├── docs/                 # Non-standard directory
├── helpers/              # Should be scripts/
└── files/                # Should be assets/
```

### Poor Naming

```
# BAD: Invalid characters
My_Skill/
Skill Generator/
api helper/
python--processor/

# BAD: Too long
this-is-a-very-long-skill-name-that-exceeds-reasonable-limits/

# BAD: Unclear purpose
helper/
utility/
tool/
```

---

## Testing Your Skills

### Validation Checklist

1. **Basic Validation**
   ```bash
   ./scripts/validate.py .
   ```

2. **Loading Test**
   ```bash
   skill skill-name --test
   ```

3. **Content Review**
   - Description length: 20-1024 characters
   - Clear trigger conditions
   - Appropriate scope (project/global)
   - Valid naming convention

4. **Structure Review**
   - Required SKILL.md file
   - Optional modular directories
   - Proper file organization
   - Executable scripts

### Common Validation Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing frontmatter | No YAML header | Add `---` YAML frontmatter |
| Invalid name | Wrong format | Use lowercase-with-hyphens |
| Long description | >1024 chars | Shorten description |
| Missing triggers | Unclear when to use | Add trigger keywords |
| Invalid directory | Wrong structure | Follow standard layout |

---

## Next Steps

1. **Choose a pattern** that matches your use case
2. **Adapt the structure** to your specific needs
3. **Test thoroughly** with validation scripts
4. **Iterate based** on real usage feedback
5. **Document patterns** for future reference

Remember: The best skills evolve based on actual usage patterns and user feedback. Start simple and add complexity as needed.