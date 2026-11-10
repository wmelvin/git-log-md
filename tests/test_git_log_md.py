"""Tests for git_log_md."""

import git_log_md


def test_git_failure_returns_nonzero(tmp_path, monkeypatch):
    """A failing `git log` (e.g. not a repository) must exit nonzero."""
    monkeypatch.chdir(tmp_path)
    assert git_log_md.main(["."]) != 0
