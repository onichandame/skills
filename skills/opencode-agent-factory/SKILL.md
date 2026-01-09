---
name: opencode-agent-factory
description: This skill should be used when users want to "create an agent", "add an agent", "write a subagent", "configure agent parameters", or need guidance on agent structure, system prompts, tool permissions, or agent development best practices.
scope: global
license: MIT
---
# OpenCode Agent Factory

## When to use this skill

Use this skill when you need to create a new OpenCode agent with specific configuration. This includes:
- Creating specialized subagents for specific domains (code review, documentation, testing)
- Defining primary agents with custom tools and permissions
- Configuring agents with specific models, temperature, or step limits
- Setting up agents with custom system prompts and behavior instructions
- Setting up specialized workflows with primary and subagent configurations

## Instructions

### Step 1: Define Agent Configuration

Create agent configuration using YAML frontmatter with the following parameters:

```yaml
---
description: (required) Brief description of what this agent does and when to use it
mode: subagent | primary | all
model: provider/model-id (e.g., "anthropic/claude-sonnet-4")
temperature: 0.0-1.0 (0.0=focused, 1.0=creative)
top_p: 0.0-1.0 (alternative sampling parameter)
steps: number (max agent iterations before text-only response)
hidden: true | false (hide from @autocomplete, subagents only)
color: "#RRGGBB" (hex color for UI)
disable: true | false
prompt: path/to/prompt.txt or inline prompt
tools:
  write: true | false
  edit: true | false
  bash: true | false
  skill: true | false
  webfetch: true | false
permission:
  edit: allow | ask | deny
  bash: allow | ask | deny | { specific-command: allow | ask | deny }
  webfetch: allow | ask | deny
  doom_loop: allow | ask | deny
  external_directory: allow | ask | deny
---
```

### Step 2: Add Agent Prompt

After frontmatter, include the agent's system prompt:

```
You are a specialized [agent type] focused on [domain/purpose].
Your responsibilities include:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

Guidelines:
- [Guideline 1]
- [Guideline 2]
```

### Step 3: Save Agent File

Save the agent definition to the appropriate location:
- **Project agents**: `.opencode/agent/<agent-name>.md`
- **Global agents**: `~/.config/opencode/agent/<agent-name>.md`

## Parameter Reference

### Mode Options
- **subagent**: Background agent, invoked by primary agents or @mention
- **primary**: Main execution agent, users interact directly
- **all**: Operates in both modes

### Temperature Guide
- **0.0-0.3**: Highly focused, deterministic responses (coding, analysis)
- **0.4-0.7**: Balanced creativity and focus (general tasks)
- **0.8-1.0**: Highly creative, exploratory responses (brainstorming)

### Tools Configuration
Available tools include:
- `write`: File creation and modification
- `edit`: File editing capabilities
- `bash`: Shell command execution
- `skill`: Skill invocation
- `webfetch`: Web content retrieval
- `mcp_*`: MCP server tools (wildcard support)

### Permission Levels
- **allow**: No confirmation required
- **ask**: User prompted for approval
- **deny**: Action blocked
- **bash** supports command-specific rules via object syntax

## Example: Code Review Agent

```yaml
---
description: Specialized agent for reviewing code changes. Performs type safety checks, evaluates code quality, and suggests improvements.
mode: subagent
temperature: 0.2
steps: 20
hidden: false
tools:
  write: false
  edit: false
  bash: false
  skill: false
  webfetch: false
permission:
  edit: deny
  bash: deny
  webfetch: deny
---
You are a code review expert focused on type safety and code quality.

Your responsibilities:
- Analyze code changes for type errors and potential bugs
- Check for type safety violations (no `as any`, `@ts-ignore`, etc.)
- Evaluate code conciseness and expressiveness
- Suggest improvements for better TypeScript/JavaScript practices
- Identify potential performance issues

Guidelines:
- Be specific about line numbers and exact issues
- Provide actionable suggestions with code examples
- Never suppress type errors with `as any`, `@ts-ignore`, or `@ts-expect-error`
- Focus on type safety, not style preferences
- Report pre-existing issues separately from new issues
```

## Example: Documentation Agent

```yaml
---
description: Creates comprehensive documentation for code, APIs, and technical concepts. Generates README files, API docs, architecture guides, and user documentation.
mode: subagent
temperature: 0.5
steps: 30
hidden: false
prompt: path/to/docs-prompt.txt
tools:
  write: true
  edit: true
  bash: false
  skill: false
  webfetch: true
permission:
  edit: allow
  bash: deny
  webfetch: allow
---
You are a technical documentation specialist.

Your responsibilities:
- Create clear, comprehensive documentation for codebases
- Write README files with getting started guides
- Document APIs with parameters, return types, and examples
- Generate architecture diagrams and flow explanations
- Maintain consistent documentation style across projects

Guidelines:
- Use clear headings and logical structure
- Include code examples where helpful
- Keep documentation up-to-date with code changes
- Prefer clarity over brevity
- Use consistent terminology throughout
```

## Example: Testing Agent

```yaml
---
description: Generates comprehensive test suites for code. Creates unit tests, integration tests, and end-to-end tests following best practices.
mode: subagent
temperature: 0.3
steps: 25
hidden: false
tools:
  write: true
  edit: true
  bash: true
  skill: false
  webfetch: false
permission:
  edit: allow
  bash: ask
  webfetch: deny
---
You are a testing specialist focused on comprehensive test coverage.

Your responsibilities:
- Generate unit tests for functions and classes
- Create integration tests for module interactions
- Write end-to-end tests for critical user flows
- Ensure high code coverage without testing trivial code
- Follow testing best practices (AAA pattern, meaningful assertions)

Guidelines:
- Test behavior, not implementation details
- Use meaningful test names that describe the scenario
- Cover happy path, edge cases, and error conditions
- Avoid testing framework internals or third-party code
- Keep tests independent and repeatable
```

## Validation Requirements

- **Agent name**: Lowercase with hyphens only, 1-64 characters (regex: `^[a-z0-9]+(-[a-z0-9]+)*$`)
- **Description**: Required, 20-1024 characters
- **Frontmatter**: Must be valid YAML with proper indentation
- **Mode**: Must be "subagent", "primary", or "all"
- **Temperature**: Must be between 0.0 and 1.0
- **Steps**: Must be a positive integer

## Advanced Configuration

### Custom Model Selection
```yaml
model: anthropic/claude-sonnet-4
# or
model: openai/gpt-4-turbo
# or
model: google/gemini-pro
```

### Command-Specific Bash Permissions
```yaml
permission:
  bash:
    git status: allow
    git add: allow
    git commit: ask
    git push: ask
    rm: deny
    *: ask  # Default for unspecified commands
```

### Color Coding
```yaml
color: "#3B82F6"  # Blue for analysis agents
color: "#10B981"  # Green for build agents  
color: "#EF4444"  # Red for security agents
color: "#F59E0B"  # Orange for exploration agents
```

## Best Practices

1. **Start with focused temperature** (0.1-0.3) for specialized agents
2. **Use specific descriptions** (20-1024 chars) for clear triggering
3. **Limit tools** to only what's necessary for the agent's purpose
4. **Set reasonable step limits** based on task complexity
5. **Hide subagents** that shouldn't be manually invoked
6. **Use ask permission** for destructive or external operations
7. **Test agents** with representative tasks before deployment

## File Locations

- **Project agents**: `.opencode/agent/<agent-name>.md`
- **Global agents**: `~/.config/opencode/agent/<agent-name>.md`
- **Project skills**: `.opencode/skill/<skill-name>/SKILL.md`
- **Global skills**: `~/.config/opencode/skill/<skill-name>/SKILL.md`

Agents and skills follow the same precedence rules: project config overrides global config.
