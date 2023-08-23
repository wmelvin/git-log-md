# git_log_md.py

Uses `git log` to create a Markdown document listing the message, hash, and timestamp for each commit.

A task list *completed item* checkmark can be added in front of commit the message using the `--do-mark` switch.

GitHub Docs: [About task lists](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/about-task-lists#creating-task-lists)

The commit hash and date can be styled as *superscript* using the `--do-sup` switch.

GitHub Docs: [styling text](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#styling-text)

### Command-Line Usage

```
usage: git_log_md.py [-h] [-u REPO_URL] [-o FILE_NAME] [-t] [--git-out]
                     [--do-mark] [--do-sup]
                     [dir_name]

Create a markdown listing commits to a Git repository at a given path.

positional arguments:
  dir_name              Name of directory containing the Git repository.

options:
  -h, --help            show this help message and exit
  -u REPO_URL, --repo-url REPO_URL
                        GitHub repository URL.
  -o FILE_NAME, --output FILE_NAME
                        Name of output file.
  -t, --timestamp       Add a timestamp (date_time) tag to the output file
                        name.
  --git-out             Print the output (STDOUT and STDERR) from running the
                        'git log' command.
  --do-mark             Add a task-list-completed-item checkmark in front of
                        the commit message.
  --do-sup              Add superscript tags around the commit hash and date.
```

### Reference 

Git Documentation: 
- [git-log - commit ordering](https://git-scm.com/docs/git-log#_commit_ordering)
- [date - format](https://git-scm.com/docs/git-rev-list#Documentation/git-rev-list.txt---dateltformatgt)
- [pretty format](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History#pretty_format)
