@default:
  @just --list

# Remove dist and egg-info
@clean:
  -rm dist/*
  -rm git_log_md.egg-info/*

# Run lint, check, and pyproject-build
@build: lint check
  uv build

#  Run ruff format --check
@check:
  uv run ruff format --check

# Run check and lint
@checks: check lint

# Run ruff format
@format: lint
  uv run ruff format

# Redirect 'git_log_md -h' to temp.txt
@help:
  uv run git_log_md -h > temp.txt

# Run ruff check
@lint:
  uv run ruff check
