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
6. Validate the generated frontmatter and ensure the description is 20-1024 characters long and speaks to when OpenCode should trigger the skill
7. Return only the generated `SKILL.md` content

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

**Basic Skill Directory:**
```
skill-name/
└── SKILL.md
```

**Complete Skill Directory (with supporting files):**
```
skill-name/
├── SKILL.md              # Required - main skill definition
├── scripts/              # Optional - executable code files
│   ├── helper.py
│   └── deploy.sh
├── references/           # Optional - documentation and resources
│   ├── api-docs.md
│   └── examples.md
└── assets/               # Optional - templates and resources
    ├── template.html
    └── config.json
```

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
```
