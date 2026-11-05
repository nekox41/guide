# Repository Guidelines

## Project Structure & Module Organization

This repository contains the GitBook-based Eidolon Guide for Warframe; its source is Markdown documentation rather than application code.

- `README.md` is the landing page; `SUMMARY.md` defines navigation.
- `basics/`, `advanced/`, and `builds/` organize mechanics and equipment advice.
- `solo-strats/` and `duo-strats/` contain strategy-specific walkthroughs.
- `zh/` contains the Chinese guide, including its own landing page and navigation.
- `.gitbook/assets/` stores images and other media.
- `vocabulary.md`, `credits.md`, `changelog.md`, and `to-do.md` provide supporting information.

## Build, Test, and Development Commands

No local build scripts, package manifest, automated test suite, or lint configuration are provided. Edit Markdown directly and inspect rendered changes in GitBook when available.

- `git diff --check`: detect whitespace errors before committing.
- `git diff --stat`: review the scope of changed files.
- `git diff -- SUMMARY.md zh/SUMMARY.md`: inspect navigation changes.
- `rg 'search term' basics/ builds/`: locate related advice before updating a mechanic.

## Coding Style & Naming Conventions

Use one descriptive `#` heading per page and subordinate headings for sections. Follow nearby pages for Markdown formatting: `*` bullets, two-space indentation for nested lists, and relative links to repository pages and assets.

Use lowercase, hyphen-separated filenames for new pages, such as `lure-management.md`; use `README.md` for section entry pages. Preserve existing YAML front matter, GitBook `{% ... %}` directives, HTML details blocks, and asset references. Avoid unrelated formatting changes.

## Testing Guidelines

Validation is manual; no automated coverage requirement is configured. Check changed links, image paths, heading anchors, and GitBook rendering. Add new reader-facing pages to the appropriate `SUMMARY.md`. When moving pages, update incoming links and navigation. Review corresponding `zh/` content for translation impact and note any remaining translation work.

## Commit & Pull Request Guidelines

Recent history consists of GitBook-generated messages such as `GITBOOK-32: change request with no subject merged in GitBook`; it does not establish a manual commit convention. For manual commits, use short, descriptive subjects such as `docs: clarify Volt solo lure timing`.

Keep pull requests focused. Describe affected pages, explain gameplay corrections, link relevant issues or supporting references, and summarize validation. Include rendered screenshots for layout or media changes and flag translation follow-ups.
