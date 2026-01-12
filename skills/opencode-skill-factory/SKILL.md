---
name: opencode-skill-factory
description: (opencode - Skill) Create and generate new OpenCode skill files with proper YAML frontmatter and Markdown structure. MUST USE when users want to create, build, or define new skills, skill files, SKILL.md files, or need to generate skill documentation.
license: MIT
---
# Skill Factory

## What this skill does
Generates complete `SKILL.md` files with proper YAML frontmatter and structured Markdown content when users want to create new OpenCode skills but don't know the required format or conventions.

## When to use this skill
Use this when:
- You want to define a new OpenCode skill
- You need correct YAML frontmatter structure
- You want to ensure the skill's description clearly triggers in OpenCode
- You need standardized structure, behavior rules, and examples
- You want to follow established formatting conventions

## Instructions
1. Ask the user for the **skill name** (must be lowercase with hyphens, no spaces)
2. Ask for a **short description** that explains what the skill does and when to use it (20-1024 characters)
3. Ask for the **scope** of the skill (project/global) to determine where it should be available
4. Ask any additional context needed for behavior — e.g., inputs, outputs, constraints
5. Generate a complete `SKILL.md` including:
   - YAML frontmatter with `name`, `description`, and `scope`
   - A Markdown body that includes:
     - A clear explanation of what the skill does
     - When it should be invoked
     - Step-by-step behavior instructions
     - Example usage if appropriate
     - **Cross-references to additional files**: For complex content >500 lines, add links like:
       - `See [references/advanced-patterns.md](references/advanced-patterns.md) for detailed examples`
       - `Refer to [references/troubleshooting.md](references/troubleshooting.md) for common issues`
6. Validate the generated frontmatter and ensure the description is 20-1024 characters long and speaks to when OpenCode should trigger the skill
7. Return only the generated `SKILL.md` content

## Progressive Loading Guidelines

### When to Use Additional Files

**Use `references/` files for:**
- Detailed examples and patterns
- Comprehensive troubleshooting guides
- Advanced techniques or edge cases
- API documentation or reference materials

**Use `assets/` files for:**
- Templates for output formatting
- Configuration files or schemas
- Reusable code snippets
- Static resources (images, icons)

### How to Reference Additional Files in SKILL.md

Use markdown cross-references to link to additional content:

```markdown
## Advanced Examples
See [references/examples.md](references/examples.md) for comprehensive usage examples.

## Troubleshooting
Refer to [references/troubleshooting.md](references/troubleshooting.md) for common issues.

## Template Usage
Use the templates in [assets/templates/](assets/templates/) for consistent output formatting.
```

**Loading Behavior:**
- `SKILL.md` loads when skill triggers
- `references/` files load only when referenced
- `assets/` files load only when explicitly accessed
- `scripts/` execute directly without loading into context

## Skill Locations and Folder Structure

### Skill Discovery Precedence Order
OpenCode searches for skills in these locations (highest to lowest priority):

1. **Project config**: `.opencode/skill/<name>/SKILL.md`
2. **Global config**: `~/.config/opencode/skill/<name>/SKILL.md`  
3. **Project Claude-compatible**: `.claude/skills/<name>/SKILL.md`
4. **Global Claude-compatible**: `~/.claude/skills/<name>/SKILL.md`

### Choosing the Right Location

**Use Project Skills (`.opencode/skill/`) when:**
- Skill is specific to a particular project
- Skill contains project-specific logic or configurations
- You want the skill to override global skills with the same name
- Skill should only be available to team members working on this project

**Use Global Skills (`~/.config/opencode/skill/`) when:**
- Skill is generally useful across multiple projects
- Skill provides common functionality (e.g., code review, documentation)
- You want the skill available everywhere
- Skill doesn't contain project-specific information

### Recommended Folder Structure

**Progressive Loading Architecture**

OpenCode skills use a three-level progressive disclosure system to optimize context usage and performance:

1. **Metadata (name + description)**: Always loaded (~100 words) for skill discovery
2. **SKILL.md body**: Loaded when skill triggers (keep under 5,000 words)
3. **Bundled resources**: Loaded on-demand as needed by Claude (unlimited size)

**Basic Skill Directory:**
```
skill-name/
└── SKILL.md              # Required - main skill definition (< 5,000 words)
```

**Complete Modular Skill Directory:**
```
skill-name/
├── SKILL.md              # Required - main skill definition
├── scripts/              # Optional - executable code files
│   ├── helper.py         # Self-contained automation scripts
│   └── deploy.sh         # Deployment automation
├── references/           # Optional - documentation for context loading
│   ├── api-docs.md       # Detailed API references
│   ├── examples.md       # Comprehensive examples
│   └── troubleshooting.md # Debug guidance
└── assets/               # Optional - templates and resources
    ├── template.html     # Output templates
    ├── config.json       # Configuration files
    └── icons/            # Visual assets
```

### Modular File Organization Best Practices

**Progressive File Loading Pattern:**
- Keep `SKILL.md` lean (under 500 lines optimal) for fast loading
- Move detailed reference documentation to `references/` directory
- Place complex examples in `references/examples.md`
- Store reusable templates in `assets/` directory
- Keep automation logic in `scripts/` directory

**Content Separation Strategy:**
- `SKILL.md`: Core instructions, triggers, and basic examples
- `references/`: Detailed documentation, patterns, troubleshooting
- `scripts/`: Validation, testing, deployment automation
- `assets/`: Templates, configurations, static resources

**Context Optimization:**
```
# Fast-loading skill structure
skill-name/
├── SKILL.md              # < 500 lines, core logic only
├── references/
│   ├── advanced-patterns.md  # Loaded when complex patterns needed
│   ├── troubleshooting.md    # Loaded when errors occur
│   └── api-reference.md      # Loaded when API details needed
└── scripts/
    └── validate.py      # Never loaded into context, executed directly
```

**File Organization Guidelines:**
- Each supporting file should serve one clear purpose
- Avoid duplication between `SKILL.md` and reference files
- Use clear, descriptive filenames
- Structure reference files for selective loading
- Keep scripts self-contained and executable

### Naming Conventions

- **Skill directory**: lowercase with hyphens only (`my-skill`, `frontend-design`)
- **SKILL.md filename**: Must be exactly `SKILL.md` (uppercase)
- **Frontmatter name**: Must match directory name exactly
- **Tool invocation**: OpenCode converts directory to tool name (e.g., `skill-name/` → `skill skill-name`)

### Precedence Behavior

- Higher priority locations override lower priority locations
- Project skills override global skills with the same name
- OpenCode locations override Claude-compatible locations
- First matching skill found is used, others are ignored

### Permissions Configuration

Skills must be enabled in OpenCode configuration:

```json
{
  "permission": {
    "skill": {
      "my-skill": "allow",
      "frontend-design": "allow",
      "experimental-*": "ask",
      "*": "deny"
    }
  }
}
```

**Permission States:**
- `allow` - Skill loads immediately and is available to agents
- `deny` - Skill is hidden from agents, access rejected
- `ask` - User prompted for approval before loading skill

**Wildcards Support:**
- Use `*` as wildcard (e.g., `internal-*` denies all skills starting with "internal-")
- More specific patterns override general patterns
- Order matters in configuration file

### Skill Validation Requirements

**Name Validation:**
- Must match directory name containing `SKILL.md`
- Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
- 1-64 characters
- Lowercase alphanumeric with single hyphen separators
- Cannot start/end with `-` or contain consecutive `--`

**Description Requirements:**
- Required: 20-1024 characters
- Should clearly indicate when OpenCode should trigger the skill
- Be specific enough for agents to choose correctly
- Include target workflow or use case

**Required Frontmatter Structure:**
```yaml
---
name: skill-name          # Required: matches directory name
description: Skill description  # Required: 20-1024 chars
license: MIT             # Optional but recommended
scope: project           # Optional: project or global
---
```

### Agent-Specific Configuration

Skills can be controlled per agent through:

**Custom Agent Frontmatter:**
- Override permissions and tool availability
- Configure specific skill access per agent type

**Built-in Agent Config:**
- Configure in `opencode.json` under `agent` section
- Set default skill availability per agent

**Oh-My-OpenCode Plugin:**
- Advanced agent-specific skill management
- Dynamic skill enabling/disabling
- Workflow-based skill selection

### Migration Notes

If migrating from Claude's skills system:
- Move from `.claude/skills/` → `.opencode/skill/` (for project skills)
- Move from `~/.claude/skills/` → `~/.config/opencode/skill/` (for global skills)
- Existing SKILL.md files work without changes
- Update permission configuration from `tools` to `permission.skill`

## Example invocation
User: "Create a skill that reviews Python code for PEP-8 style issues."

**Result**: The skill-factory produces a complete SKILL.md with proper frontmatter and behavior instructions.

## Updating Existing Skills

### When to Update Skills

Update skills when:
- Adding new functionality or capabilities
- Fixing bugs or improving behavior
- Updating for new OpenCode versions
- Refining based on real usage feedback
- Improving documentation or examples

### Skill Update Workflow

**Step 1: Backup Current Skill**
```bash
# Create backup before major changes
cp -r skill-name skill-name.backup-$(date +%Y%m%d)
```

**Step 2: Choose Update Strategy**

**Minor Updates (Documentation, Examples):**
1. Edit `SKILL.md` directly
2. Update reference files in `references/`
3. Test with validation script
4. Version bump (patch)

**Major Updates (Structure, Logic):**
1. Create new modular structure if missing
2. Move detailed content to appropriate directories
3. Update automation scripts
4. Comprehensive testing
5. Version bump (minor/major)

**Step 3: Validate Changes**
```bash
# Run skill validation
./scripts/validate.py skill-name/

# Test skill loading
skill skill-name --test

# Verify syntax
yamllint skill-name/SKILL.md
```

**Step 4: Version Management**

**Semantic Versioning for Skills:**
- `MAJOR.MINOR.PATCH` (e.g., 1.2.3)
- MAJOR: Breaking changes, new architecture
- MINOR: New features, backward compatible
- PATCH: Bug fixes, documentation improvements

**Update Strategy Options:**

1. **In-Place Update** (Patch/Minor):
   - Directly edit existing files
   - Maintain same directory structure
   - Suitable for non-breaking changes

2. **Parallel Development** (Major):
   - Create `skill-name-v2/` alongside original
   - Test thoroughly before migration
   - Migrate when ready, archive old version

3. **Incremental Migration** (Complex):
   - Create modular structure gradually
   - Move content piece by piece
   - Maintain backward compatibility during transition

### Progressive Loading Implementation

**Converting Single-File to Modular:**

1. **Analyze Current Content:**
   ```bash
   # Check current file size
   wc -l skill-name/SKILL.md
   
   # Identify sections to extract
   grep -n "##" skill-name/SKILL.md
   ```

2. **Create Modular Structure:**
   ```bash
   mkdir -p skill-name/{scripts,references,assets}
   
   # Move detailed examples
   sed -n '/## Examples/,$p' skill-name/SKILL.md > skill-name/references/examples.md
   
   # Keep core in SKILL.md
   sed -i '/## Examples/,$d' skill-name/SKILL.md
   echo '## Examples\nSee [references/examples.md](references/examples.md) for detailed examples.' >> skill-name/SKILL.md
   ```

3. **Update References:**
   ```markdown
   <!-- In SKILL.md -->
   ## Advanced Patterns
   See [references/advanced-patterns.md](references/advanced-patterns.md) for comprehensive pattern documentation.
   
   ## Troubleshooting
   Refer to [references/troubleshooting.md](references/troubleshooting.md) for common issues.
   ```

**Content Migration Guidelines:**
- Move content > 500 lines to reference files
- Keep essential triggers and basic instructions in `SKILL.md`
- Use cross-references between files
- Test each migration step

### Testing and Validation

**Automated Validation:**
```python
# scripts/validate.py
import yaml
import re
import os

def validate_skill(skill_path):
    """Validate skill structure and content"""
    errors = []
    
    # Check required files
    if not os.path.exists(f"{skill_path}/SKILL.md"):
        errors.append("Missing SKILL.md")
    
    # Validate frontmatter
    with open(f"{skill_path}/SKILL.md") as f:
        content = f.read()
        try:
            frontmatter = yaml.safe_load(content.split('---')[1])
            validate_frontmatter(frontmatter, errors)
        except Exception as e:
            errors.append(f"Invalid YAML: {e}")
    
    return errors
```

**Manual Testing Checklist:**
- [ ] Skill loads without errors
- [ ] Description triggers appropriately
- [ ] All examples work as expected
- [ ] Reference files load correctly
- [ ] Scripts execute successfully
- [ ] No broken links or references

### Configuration Updates

**Maintain Configuration During Updates:**
Back up and preserve user configurations:
```bash
# Export current permissions
opencode config get permission.skill > permissions-backup.json

# After update, restore if needed
opencode config set permission.skill "$(cat permissions-backup.json)"
```

**Version Pinning (Advanced):**
```json
{
  "skill": {
    "my-skill": {
      "permission": "allow",
      "version": ">=1.2.0,<2.0.0"
    }
  }
}
```

### Rollback Procedures

**Quick Rollback:**
```bash
# Restore from backup
rm -rf skill-name
mv skill-name.backup-YYYYMMDD skill-name
```

**Git-Based Rollback:**
```bash
# If using version control
git checkout HEAD~1 -- skill-name/
```

### Update Notification Pattern

**Communicate Changes:**
```markdown
## Changelog

### v1.2.0 (2024-01-15)
- Added modular file structure support
- Improved pattern documentation
- Updated validation scripts

### v1.1.0 (2024-01-01)
- Enhanced example coverage
- Fixed bug in trigger detection

### v1.0.0 (2023-12-15)
- Initial release
```

## Example output
```markdown
---
name: python-style-review
description: Review a Python file for PEP-8 compliance and provide a list of violations with suggestions on how to fix them.
scope: project
license: MIT
---
# Python Style Review

## When to use this skill
When a user needs a PEP-8 style analysis of a Python file.

## Instructions
1. Take the provided Python source code as input
2. Analyze for PEP-8 violations using common style rules
3. Output a structured list of issues with line numbers and suggestions

## Advanced Patterns
See [references/advanced-patterns.md](references/advanced-patterns.md) for complex PEP-8 scenarios.

## Troubleshooting
Refer to [references/troubleshooting.md](references/troubleshooting.md) for common analysis issues.
```
