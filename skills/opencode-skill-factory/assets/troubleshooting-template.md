# Troubleshooting Template

This template provides a structured approach to documenting common issues and solutions for your skill.

## Common Problems

### Problem: Skill Not Triggering

**Symptoms:**
- Skill doesn't activate when expected
- Agent doesn't recognize relevant inputs
- No response to skill-specific queries

**Common Causes:**
- [ ] Description doesn't clearly indicate when to trigger
- [ ] Missing trigger keywords (when, use, apply, etc.)
- [ ] Description is too vague or generic
- [ ] Skill permissions not configured correctly

**Solutions:**
1. **Review Description:** Ensure description clearly states when to use the skill
2. **Add Trigger Words:** Include phrases like "Use when..." or "Apply for..."
3. **Check Permissions:** Verify skill is enabled in configuration
4. **Test Loading:** Run validation script to ensure skill loads properly

**Example Fix:**
```yaml
# Before (vague)
description: Helps with code analysis

# After (clear trigger)
description: Analyze code for security vulnerabilities and performance issues. Use when you need comprehensive code review or want to identify potential problems.
```

### Problem: Incorrect Output Format

**Symptoms:**
- Output doesn't match expected format
- Missing required information
- Structure varies between runs

**Common Causes:**
- [ ] Instructions are too general or ambiguous
- [ ] Missing format specifications in instructions
- [ ] No clear output examples provided
- [ ] Complex instructions not broken into steps

**Solutions:**
1. **Add Format Requirements:** Specify exact output format in instructions
2. **Include Examples:** Add clear examples of expected output
3. **Break Down Steps:** Make instructions more specific and sequential
4. **Add Validation:** Include self-check steps in instructions

**Example Fix:**
```markdown
# Before (general)
## Instructions
Analyze the code and provide feedback.

# After (specific)
## Instructions
1. Parse the provided code structure
2. Check for {specific issues}
3. Output results in this format:
   ```
   ## Issues Found
   - Line X: {description}
   - Line Y: {description}
   
   ## Recommendations
   1. {action item}
   2. {action item}
   ```
```

### Problem: Skill Over-Triggering

**Symptoms:**
- Skill activates for unrelated queries
- Interferes with other skills
- Context pollution

**Common Causes:**
- [ ] Description is too broad
- [ ] Matches too many input patterns
- [ ] Lacks specific domain constraints

**Solutions:**
1. **Narrow Scope:** Make description more specific to particular use cases
2. **Add Constraints:** Include specific domains or conditions
3. **Use Precise Language:** Avoid generic terms

**Example Fix:**
```yaml
# Before (too broad)
description: Provides analysis and insights

# After (specific)
description: Analyze Python web applications for Django-specific security vulnerabilities. Use when reviewing Django codebases or deploying Django applications to production.
```

## Debugging Workflow

### Step 1: Validation Check
```bash
# Run comprehensive validation
./scripts/validate.py .

# Check for syntax errors
yamllint SKILL.md
```

### Step 2: Loading Test
```bash
# Test skill loading
skill skill-name --test

# Check permissions
opencode config get permission.skill
```

### Step 3: Manual Testing
1. **Simple Input:** Test with basic, unambiguous input
2. **Edge Cases:** Try boundary conditions and unusual inputs
3. **Complex Scenarios:** Test with realistic, complex inputs
4. **Negative Testing:** Try inputs that should NOT trigger

### Step 4: Log Analysis
- Check system logs for skill activation
- Review context window usage
- Monitor performance metrics

## Performance Issues

### Problem: Slow Response Times

**Common Causes:**
- [ ] SKILL.md too long (exceeds 500 lines)
- [ ] Complex instruction logic
- [ ] Missing progressive loading structure

**Solutions:**
1. **Optimize Content:** Move detailed content to reference files
2. **Implement Progressive Loading:** Use modular structure
3. **Simplify Instructions:** Break complex logic into clearer steps

### Progressive Loading Implementation

**Before (Monolithic):**
```markdown
---
name: complex-skill
description: Handles complex processing tasks
---
# Complex Skill

## Basic Instructions
[200+ lines of detailed instructions...]

## Advanced Patterns
[300+ lines of advanced content...]

## Troubleshooting
[200+ lines of troubleshooting...]

## Examples
[400+ lines of examples...]
```

**After (Progressive):**
```markdown
---
name: complex-skill
description: Handles complex processing tasks. Use when you need advanced data processing capabilities.
---
# Complex Skill

## What this skill does
Processes complex data through specialized algorithms.

## When to use this skill
Use when you need advanced data processing.

## Instructions
1. Analyze input requirements
2. Select processing algorithm
3. Execute transformation
4. Format output

## Advanced Patterns
See [references/advanced-patterns.md](references/advanced-patterns.md) for detailed strategies.

## Troubleshooting
Refer to [references/troubleshooting.md](references/troubleshooting.md) for common issues.

## Examples
Detailed examples available in [references/examples.md](references/examples.md).
```

## Maintenance Guidelines

### Regular Reviews
- [ ] **Monthly:** Test skill with new inputs and edge cases
- [ ] **Quarterly:** Review and update examples based on usage
- [ ] **Annually:** Evaluate skill relevance and update for new features

### Update Process
1. **Backup:** Create backup before major changes
2. **Test Changes:** Validate with validation script
3. **Incremental Updates:** Make changes gradually
4. **Documentation:** Keep examples and docs updated

### Monitoring
- Track skill usage patterns
- Monitor success/failure rates
- Collect user feedback
- Update based on real usage

## Getting Help

### Self-Service Resources
1. **Examples:** Review `references/examples.md` for usage patterns
2. **Validation:** Run `./scripts/validate.py .` for health check
3. **Community:** Check for similar skills and patterns

### When to Escalate
- Skill consistently fails validation
- Performance issues after optimization attempts
- Complex integration problems
- Security or compliance concerns

---

## Usage Instructions

1. Copy this template to `references/troubleshooting.md` in your skill directory
2. Customize sections with skill-specific information
3. Add new problems as you encounter them
4. Update solutions based on actual debugging experience
5. Review quarterly to ensure accuracy

Remember: Good troubleshooting documentation reduces support overhead and improves user experience!