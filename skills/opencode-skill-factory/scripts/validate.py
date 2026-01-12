#!/usr/bin/env python3
"""
Skill Validation Script for OpenCode Skills

Validates skill structure, frontmatter, and content according to best practices.
Usage: python validate.py <skill_path>
"""

import os
import sys
import yaml
import re
import json
from pathlib import Path
from typing import List, Dict, Any


class SkillValidator:
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path).resolve()
        self.errors = []
        self.warnings = []
        self.info = []

    def validate(self) -> Dict[str, Any]:
        """Run all validations and return results"""
        self._validate_structure()
        self._validate_skill_file()
        self._validate_frontmatter()
        self._validate_content()
        self._validate_optional_structure()

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
        }

    def _validate_structure(self):
        """Validate basic directory structure"""
        if not self.skill_path.exists():
            self.errors.append(f"Skill directory does not exist: {self.skill_path}")
            return

        if not self.skill_path.is_dir():
            self.errors.append(f"Path is not a directory: {self.skill_path}")
            return

        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.errors.append("Missing required SKILL.md file")
        elif not skill_md.is_file():
            self.errors.append("SKILL.md exists but is not a file")

    def _validate_skill_file(self):
        """Validate SKILL.md file structure"""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return

        try:
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for YAML frontmatter
            if not content.startswith("---\n"):
                self.errors.append("SKILL.md must start with YAML frontmatter (---\\n)")
                return

            # Extract frontmatter
            parts = content.split("---\n")
            if len(parts) < 3:
                self.errors.append("SKILL.md frontmatter must be closed with ---")
                return

            frontmatter_str = parts[1]
            body_content = "---\n".join(parts[2:])

            # Store for later validation
            self.frontmatter_str = frontmatter_str
            self.body_content = body_content
            self.full_content = content

        except Exception as e:
            self.errors.append(f"Error reading SKILL.md: {e}")

    def _validate_frontmatter(self):
        """Validate YAML frontmatter content"""
        if not hasattr(self, "frontmatter_str"):
            return

        try:
            frontmatter = yaml.safe_load(self.frontmatter_str)
            if not isinstance(frontmatter, dict):
                self.errors.append("Frontmatter must be a YAML dictionary")
                return

            self.frontmatter = frontmatter

            # Required fields
            if "name" not in frontmatter:
                self.errors.append("Missing required field: name")
            else:
                self._validate_name(frontmatter["name"])

            if "description" not in frontmatter:
                self.errors.append("Missing required field: description")
            else:
                self._validate_description(frontmatter["description"])

            # Optional fields
            if "license" in frontmatter:
                self._validate_license(frontmatter["license"])

            if "scope" in frontmatter:
                self._validate_scope(frontmatter["scope"])

        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in frontmatter: {e}")

    def _validate_name(self, name: str):
        """Validate skill name"""
        if not isinstance(name, str):
            self.errors.append("name must be a string")
            return

        # Check against directory name
        if name != self.skill_path.name:
            self.errors.append(
                f"name '{name}' must match directory name '{self.skill_path.name}'"
            )

        # Regex validation
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
            self.errors.append(
                "name must contain only lowercase letters, numbers, and single hyphens"
            )

        if len(name) < 1 or len(name) > 64:
            self.errors.append("name must be 1-64 characters long")

        if name.startswith("-") or name.endswith("-"):
            self.errors.append("name cannot start or end with a hyphen")

        if "--" in name:
            self.errors.append("name cannot contain consecutive hyphens")

    def _validate_description(self, description: str):
        """Validate skill description"""
        if not isinstance(description, str):
            self.errors.append("description must be a string")
            return

        desc_len = len(description)
        if desc_len < 20:
            self.errors.append("description must be at least 20 characters long")
        elif desc_len > 1024:
            self.errors.append("description must not exceed 1024 characters")

        # Check for trigger indication
        trigger_words = ["when", "use", "trigger", "invoke", "call", "apply"]
        if not any(word in description.lower() for word in trigger_words):
            self.warnings.append(
                "description should indicate when to trigger the skill"
            )

    def _validate_license(self, license_str: str):
        """Validate license field"""
        if not isinstance(license_str, str):
            self.errors.append("license must be a string")
            return

        common_licenses = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "ISC"]
        if license_str not in common_licenses:
            self.warnings.append(
                f"Consider using a standard license (e.g., {', '.join(common_licenses)})"
            )

    def _validate_scope(self, scope: str):
        """Validate scope field"""
        if not isinstance(scope, str):
            self.errors.append("scope must be a string")
            return

        if scope not in ["project", "global"]:
            self.errors.append("scope must be either 'project' or 'global'")

    def _validate_content(self):
        """Validate skill body content"""
        if not hasattr(self, "body_content"):
            return

        # Check for required sections
        required_sections = [
            "## What this skill does",
            "## When to use this skill",
            "## Instructions",
        ]
        for section in required_sections:
            if section not in self.body_content:
                self.warnings.append(f"Consider adding section: {section}")

        # Content length check
        lines = len(self.body_content.split("\n"))
        if lines > 500:
            self.warnings.append(
                f"SKILL.md is quite long ({lines} lines). Consider moving detailed content to reference files"
            )

        # Check for examples
        if (
            "## Example" not in self.body_content
            and "## Examples" not in self.body_content
        ):
            self.info.append("Consider adding examples to improve skill usability")

    def _validate_optional_structure(self):
        """Validate optional directory structure"""
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists():
            if not scripts_dir.is_dir():
                self.errors.append("scripts exists but is not a directory")
            else:
                # Validate script files
                for script_file in scripts_dir.iterdir():
                    if script_file.is_file() and script_file.suffix in [".py", ".sh"]:
                        self._validate_script_file(script_file)

        references_dir = self.skill_path / "references"
        if references_dir.exists():
            if not references_dir.is_dir():
                self.errors.append("references exists but is not a directory")
            else:
                self.info.append(
                    f"Found {len(list(references_dir.iterdir()))} files in references/"
                )

        assets_dir = self.skill_path / "assets"
        if assets_dir.exists():
            if not assets_dir.is_dir():
                self.errors.append("assets exists but is not a directory")
            else:
                self.info.append(
                    f"Found {len(list(assets_dir.iterdir()))} files in assets/"
                )

    def _validate_script_file(self, script_file: Path):
        """Validate individual script files"""
        if script_file.suffix == ".py":
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    script_content = f.read()
                compile(script_content, script_file, "exec")
                self.info.append(f"Python script {script_file.name} syntax is valid")
            except SyntaxError as e:
                self.errors.append(f"Syntax error in {script_file.name}: {e}")

        elif script_file.suffix == ".sh":
            # Make shell scripts executable
            try:
                script_file.chmod(0o755)
                self.info.append(f"Made shell script {script_file.name} executable")
            except Exception as e:
                self.warnings.append(
                    f"Could not make {script_file.name} executable: {e}"
                )


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate.py <skill_path>")
        sys.exit(1)

    skill_path = sys.argv[1]
    validator = SkillValidator(skill_path)

    result = validator.validate()

    # Print results
    if not result["valid"]:
        print("❌ Skill validation FAILED")
        for error in result["errors"]:
            print(f"  ERROR: {error}")
    else:
        print("✅ Skill validation PASSED")

    for warning in result["warnings"]:
        print(f"  ⚠️  WARNING: {warning}")

    for info in result["info"]:
        print(f"  ℹ️  INFO: {info}")

    # Exit with error code if validation failed
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
