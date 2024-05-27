@default:
  @just --list

# Remove dist and egg-info
@clean:
  -rm dist/*
  -rmdir dist
  -rm git_log_md.egg-info/*
  -rmdir git_log_md.egg-info

# Run lint, check, and pyproject-build
@build: lint check
  pipenv run pyproject-build

#  Run ruff format --check
@check:
  pipenv run ruff format --check

# Run check and lint
@checks: check lint

# Run ruff format
@format: lint
  pipenv run ruff format

# Run ruff check
@lint:
  pipenv run ruff check
