#!/usr/bin/env python3
"""
Skill Generation Script for OpenCode Skills

Generates new skill files interactively based on user input.
Usage: python generate.py
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
import subprocess


class SkillGenerator:
    def __init__(self):
        self.skill_info = {}

    def run(self):
        """Run interactive skill generation"""
        print("🔧 OpenCode Skill Generator")
        print("=" * 40)

        self._collect_skill_info()
        self._validate_info()
        self._generate_skill()
        self._validate_generated_skill()

        print(f"\n✅ Skill '{self.skill_info['name']}' generated successfully!")
        print(f"📍 Location: {self.skill_info['path']}")
        print(f"📝 Edit {self.skill_info['path']}/SKILL.md to customize instructions")

    def _collect_skill_info(self):
        """Collect skill information from user"""
        while True:
            name = input("Skill name (lowercase-with-hyphens): ").strip()
            if self._validate_name(name):
                self.skill_info["name"] = name
                break
            else:
                print(
                    "❌ Invalid name. Use lowercase letters, numbers, and single hyphens only."
                )

        while True:
            description = input("Description (20-1024 chars, when to use): ").strip()
            if 20 <= len(description) <= 1024:
                self.skill_info["description"] = description
                break
            else:
                print(
                    f"❌ Description must be 20-1024 characters (current: {len(description)})"
                )

        # Optional scope
        scope = input("Scope (project/global, default: project): ").strip() or "project"
        if scope in ["project", "global"]:
            self.skill_info["scope"] = scope
        else:
            print("⚠️  Invalid scope, using 'project'")
            self.skill_info["scope"] = "project"

        # Optional license
        license_default = "MIT"
        license_input = (
            input(f"License (default: {license_default}): ").strip() or license_default
        )
        self.skill_info["license"] = license_input

        # Determine path location
        location = (
            input("Location (1=project, 2=global, default: project): ").strip() or "1"
        )
        if location == "2":
            self.skill_info["path"] = (
                Path.home() / ".config" / "opencode" / "skill" / self.skill_info["name"]
            )
        else:
            self.skill_info["path"] = (
                Path.cwd() / ".opencode" / "skill" / self.skill_info["name"]
            )

    def _validate_name(self, name: str) -> bool:
        """Validate skill name format"""
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
            return False
        if len(name) < 1 or len(name) > 64:
            return False
        return True

    def _validate_info(self):
        """Validate collected information"""
        if not all(
            field in self.skill_info
            for field in ["name", "description", "scope", "license", "path"]
        ):
            raise ValueError("Missing required skill information")

    def _generate_skill(self):
        """Generate skill files and directories"""
        skill_path = self.skill_info["path"]

        # Create directory structure
        skill_path.mkdir(parents=True, exist_ok=True)
        (skill_path / "scripts").mkdir(exist_ok=True)
        (skill_path / "references").mkdir(exist_ok=True)
        (skill_path / "assets").mkdir(exist_ok=True)

        # Generate SKILL.md
        self._generate_skill_md()

        # Generate reference files
        self._generate_reference_files()

        # Generate basic validation script
        self._generate_validation_script()

    def _generate_skill_md(self):
        """Generate main SKILL.md file"""
        skill_path = self.skill_info["path"]

        content = f"""---
name: {self.skill_info["name"]}
description: {self.skill_info["description"]}
license: {self.skill_info["license"]}
scope: {self.skill_info["scope"]}
---
# {self.skill_info["name"].replace("-", " ").title()}

## What this skill does
[Describe what this skill accomplishes in 1-2 sentences]

## When to use this skill
Use this when:
- [Specific condition 1]
- [Specific condition 2]
- [Specific condition 3]

## Instructions
1. [Step 1 - what to do first]
2. [Step 2 - what to do next]
3. [Step 3 - final steps]

## Examples
[Provide clear examples of how this skill should be used]

## Additional Information
[Any additional context, constraints, or important notes]
"""

        with open(skill_path / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(content)

    def _generate_reference_files(self):
        """Generate reference documentation files"""
        skill_path = self.skill_info["path"]

        # Examples reference
        examples_content = f"""# Examples for {self.skill_info["name"]}

This file contains detailed examples and use cases for the {self.skill_info["name"]} skill.

## Basic Usage

[Example 1: Basic scenario]
```
User input: [example user input]
Expected output: [example expected output]
```

## Advanced Usage

[Example 2: Advanced scenario]
```
User input: [complex user input]
Expected output: [complex expected output]
```

## Edge Cases

[Example 3: Edge case handling]
```
User input: [edge case input]
Expected output: [edge case handling]
```
"""

        with open(
            skill_path / "references" / "examples.md", "w", encoding="utf-8"
        ) as f:
            f.write(examples_content)

        # Troubleshooting reference
        troubleshooting_content = f"""# Troubleshooting {self.skill_info["name"]}

Common issues and solutions for the {self.skill_info["name"]} skill.

## Common Problems

### Problem: [Problem description]
**Symptoms**: [What you observe]
**Causes**: [Why it happens]
**Solutions**: [How to fix it]

### Problem: Skill not triggering
**Symptoms**: Skill doesn't activate when expected
**Causes**: 
- Description doesn't clearly indicate when to trigger
- Missing trigger keywords
- Incorrect permissions

**Solutions**:
1. Update description to include clear trigger words (when, use, apply)
2. Check permission configuration
3. Verify skill loading with validation script

### Problem: Incorrect output format
**Symptoms**: Output doesn't match expected format
**Causes**: 
- Unclear instructions in SKILL.md
- Missing examples
- Ambiguous behavior guidelines

**Solutions**:
1. Add specific format instructions
2. Include clear examples in SKILL.md
3. Review and refine step-by-step instructions

## Debugging Steps

1. Run validation script: `./scripts/validate.py .`
2. Test with simple inputs
3. Check system logs for errors
4. Verify permissions and configuration

## Getting Help

If you continue experiencing issues:
1. Check the troubleshooting logs
2. Review the examples in `references/examples.md`
3. Test with different input scenarios
4. Update skill instructions based on test results
"""

        with open(
            skill_path / "references" / "troubleshooting.md", "w", encoding="utf-8"
        ) as f:
            f.write(troubleshooting_content)

    def _generate_validation_script(self):
        """Generate a basic validation script"""
        skill_path = self.skill_info["path"]

        script_content = f'''#!/usr/bin/env python3
"""
Basic validation script for {self.skill_info["name"]} skill
"""

import sys
import os
from pathlib import Path

# Add parent script directory to path for main validator
parent_scripts = Path(__file__).parent.parent.parent / "skills" / "opencode-skill-factory" / "scripts"
sys.path.insert(0, str(parent_scripts))

try:
    from validate import SkillValidator
    
    def main():
        """Validate this skill"""
        skill_path = Path(__file__).parent.parent
        validator = SkillValidator(skill_path)
        result = validator.validate()
        
        if not result['valid']:
            print("❌ Skill validation FAILED")
            for error in result['errors']:
                print(f"  ERROR: {{error}}")
            sys.exit(1)
        else:
            print("✅ Skill validation PASSED")
            
        for warning in result['warnings']:
            print(f"  ⚠️  WARNING: {{warning}}")
        
        for info in result['info']:
            print(f"  ℹ️  INFO: {{info}}")
    
    if __name__ == "__main__":
        main()
        
except ImportError:
    print("⚠️  Main validation script not found. Install opencode-skill-factory to enable validation.")
    print("   Basic checks:")
    
    # Basic checks
    skill_path = Path(__file__).parent.parent
    skill_md = skill_path / "SKILL.md"
    
    if skill_md.exists():
        print(f"✅ SKILL.md exists")
        with open(skill_md) as f:
            content = f.read()
            if content.startswith('---\\n'):
                print(f"✅ Frontmatter detected")
            else:
                print(f"❌ No frontmatter found")
    else:
        print(f"❌ SKILL.md missing")
'''

        with open(skill_path / "scripts" / "validate.py", "w", encoding="utf-8") as f:
            f.write(script_content)

        # Make executable
        os.chmod(skill_path / "scripts" / "validate.py", 0o755)


def _validate_generated_skill(self):
    """Validate the generated skill"""
    print("\n🔍 Validating generated skill...")

    # Run validation script
    skill_path = self.skill_info["path"]
    validate_script = skill_path / "scripts" / "validate.py"

    if validate_script.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(validate_script), str(skill_path)],
                capture_output=True,
                text=True,
                cwd=skill_path,
            )

            if result.returncode == 0:
                print("✅ Skill passed validation")
                if result.stdout:
                    print(result.stdout)
            else:
                print("⚠️  Skill validation warnings:")
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr)
        except Exception as e:
            print(f"⚠️  Could not run validation: {e}")
    else:
        print("⚠️  Validation script not found")


def main():
    generator = SkillGenerator()
    try:
        generator.run()
    except KeyboardInterrupt:
        print("\n❌ Skill generation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
