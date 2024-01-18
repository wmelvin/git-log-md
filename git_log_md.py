#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

app_name = Path(__file__).name

app_version = "2024.01.1"

run_dt = datetime.now()


class AppOptions(NamedTuple):
    run_dir: Path
    repo_url: str
    output_file: Path
    git_out: bool
    do_mark: bool
    do_sup: bool


def get_args(arglist=None):
    ap = argparse.ArgumentParser(
        description="Create a markdown listing commits to a Git repository "
        "at a given path."
    )

    ap.add_argument(
        "dir_name",
        nargs="?",
        help="Name of directory containing the Git repository.",
    )

    ap.add_argument(
        "-u",
        "--repo-url",
        dest="repo_url",
        type=str,
        action="store",
        help="GitHub repository URL.",
    )

    ap.add_argument(
        "-o",
        "--output",
        dest="file_name",
        type=str,
        action="store",
        help="Name of output file.",
    )

    ap.add_argument(
        "-t",
        "--timestamp",
        dest="dt_tag",
        action="store_true",
        help="Add a timestamp (date_time) tag to the output file name.",
    )

    ap.add_argument(
        "--git-out",
        dest="git_out",
        action="store_true",
        help="Print the output (STDOUT and STDERR) from running the 'git log' "
        "command.",
    )

    ap.add_argument(
        "--do-mark",
        dest="do_mark",
        action="store_true",
        help="Add a task-list-completed-item checkmark in front of the "
        "commit message.",
    )

    ap.add_argument(
        "--do-sup",
        dest="do_sup",
        action="store_true",
        help="Add superscript tags around the commit hash and date.",
    )

    return ap.parse_args(arglist)


def get_opts(arglist=None) -> AppOptions:
    args = get_args(arglist)

    if args.dir_name is None:
        dir_path = Path.cwd()
    else:
        dir_path = Path(args.dir_name).expanduser().resolve()

    if not dir_path.is_dir():
        sys.stderr.write(f"ERROR - Not a directory: '{dir_path}'\n")
        sys.exit(1)

    repo_url = args.repo_url if args.repo_url else ""

    if args.file_name is None:
        out_path = Path.cwd() / "git-log-output.md"
    else:
        out_path = Path(args.file_name).expanduser().resolve()

    if not out_path.parent.exists():
        sys.stderr.write(f"ERROR - Cannot find output directory: '{out_path.parent}'\n")
        sys.exit(1)

    if args.dt_tag:
        dt = run_dt.strftime("%Y%m%d_%H%M%S")
        out_path = out_path.with_suffix(f".{dt}{out_path.suffix}")

    return AppOptions(
        dir_path, repo_url, out_path, args.git_out, args.do_mark, args.do_sup
    )


def run_git(opts: AppOptions, args) -> subprocess.CompletedProcess:
    assert isinstance(args, list)  # noqa: S101

    git_exe = shutil.which("git")

    if git_exe is None:
        sys.stderr.write(
            "ERROR - Cannot find 'git' command. Make sure Git is installed.\n"
        )
        sys.exit(1)

    cmds = [git_exe, *args]

    result = subprocess.run(
        cmds,  # noqa: S603
        cwd=str(opts.run_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=True,
    )

    if opts.git_out:
        if result.stdout is not None:
            print(f"\nSTDOUT:\n{result.stdout.strip()}\n")

        if result.stderr is not None:
            print(f"\nSTDERR:\n{result.stderr.strip()}\n")

    return result


def as_markdown(opts: AppOptions, git_output: str) -> str:
    md = []
    lines = git_output.split("\n")

    if opts.do_sup:
        sup1 = "<sup>"
        sup2 = "</sup>"
    else:
        sup1 = ""
        sup2 = ""

    marker = "- [x] " if opts.do_mark else ""

    for line in lines:
        commit_hash, abbrev_hash, dts, msg = line.strip('"').split(" ", 3)
        dt = datetime.fromisoformat(dts).strftime("%Y-%m-%d %H:%M:%S")
        if opts.repo_url:
            url = f"{opts.repo_url}/commit/{commit_hash}"
            text = (
                f"{marker}**{msg}**\n{sup1}Commit [{abbrev_hash}]({url}) ({dt})"
                f"{sup2}\n\n---\n"
            )
        else:
            text = (
                f"{marker}**{msg}**\n{sup1}Commit *{abbrev_hash}* ({dt})"
                f"{sup2}\n\n---\n"
            )
        md.append(text)

    return "\n".join(md)


def main(arglist=None):
    print(f"\n{app_name} (v.{app_version})")

    opts = get_opts(arglist)

    print(f"\nRun 'git log' in '{opts.run_dir}'")

    result = run_git(
        opts,
        [
            "log",
            "--topo-order",
            "--reverse",
            "--date=iso-strict",
            '--pretty=format:"%H %h %ad %s"',
        ],
    )

    #  --pretty=format:
    #  %H  = Commit hash
    #  %h  = Abbreviated commit hash
    #  %ad = Author date
    #  %s  = Subject (commit message)

    if result is None:
        print("ERROR: Failed to run git command.")
    elif result.returncode == 0:
        doc = as_markdown(opts, result.stdout)
        print(f"\nWriting '{opts.output_file}'\n")
        opts.output_file.write_text(doc)
    else:
        print(f"ERROR ({result.returncode})")
        if result.stderr is not None:
            print(f"STDERR:\n{result.stderr}\n")
        if result.stdout is not None:
            print(f"STDOUT:\n{result.stdout}\n")

    return 0


if __name__ == "__main__":
    main()
