---
name: aur-bundler
description: Creates Arch Linux packages (PKGBUILD) for AUR submission. Use when users want to "package for AUR", "create PKGBUILD", "build AUR package", "submit to AUR", or need Arch packaging for software projects.
scope: global
license: MIT
---

# AUR Bundler Skill

## When to use this skill
Use this skill when users need to:
- Create PKGBUILD files for AUR submission
- Package software projects for Arch Linux
- Convert GitHub/GitLab projects into installable AUR packages
- Build Rust, Python, CMake, Autotools, or other projects for AUR
- Generate AUR metadata (.SRCINFO) and validate packages
- Handle VCS packages (git, svn) or regular releases

**Triggers**: "AUR", "PKGBUILD", "Arch package", "aur-bundler", "package for Arch", "submit to AUR", "create AUR package"

**Never use for**: General package installation, system package management, non-Arch systems

## Instructions

### Step 1: Analyze Project Structure
- Identify build system (Cargo.toml, package.json, Makefile, CMakeLists.txt, setup.py)
- Extract metadata: name, version, description, license, URL
- List all dependencies (runtime, build-time, optional)
- Check for VCS needs (git, svn) or static releases

### Step 2: Create PKGBUILD
Generate main build script with:
- **Mandatory fields**: pkgname, pkgver, pkgrel, arch, pkgdesc, url, license
- **Source**: Release tarball URL or VCS URL with branch/tag
- **Checksums**: sha256sums for releases, SKIP for VCS
- **Dependencies**: depends, makedepends, checkdepends, optdepends

### Step 3: Implement Build Functions
```bash
build() {
  cd "$pkgname-$pkgver"
  # Build commands based on project type
}

package() {
  cd "$pkgname-$pkgver"
  # Install to $pkgdir with correct paths
}
```

### Step 4: Test and Validate
- Test build: `makepkg --nodeps --skippgpcheck`
- Generate checksums: `makepkg -g >> PKGBUILD`
- Validate: `namcap PKGBUILD`
- Generate metadata: `makepkg --printsrcinfo > .SRCINFO`

### Step 5: AUR Submission
- Set up Git repository with PKGBUILD and .SRCINFO
- Configure SSH for AUR access
- Push to AUR git repository

## Tools Required
- `makepkg`: Package building (pacman)
- `namcap`: PKGBUILD validation
- `git`: For VCS packages and AUR submission
- Build tools: `base-devel`, `cargo`, `rust`, `cmake`, etc.
