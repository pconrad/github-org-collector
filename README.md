# github-org-collector
A set of scripts, based on PyGithub, to collect files with particular naming conventions from a github org


# External dependencies

You need to be able to install the Python add-on library pygithub with `pip`.

If the following commands fail, see [installing_pip.md](installing_pip.md) for hints.

For example:
```
pip install pygithub
```

If you are working on a Unix system where don't have sudo privileges, you might have success with this command; it only installs pygithub for the current user (by placing files in a hidden directory in the user's `$HOME` directory:

```
pip install --user pygithub
```

# Usage

## `collect-private.py`

### Usage:

```
python collect-private.py org-name repo-pattern file-pattern destination
```

### Use case:

* You have owner privileges to a github repo (e.g. for an academic course)
* There are private repos in that organization (e.g. for students/pairs/teams in the course)
* You want to collect some files with particular names from particular repos in that organization, and you can
    specify which ones by means of a repo-naming-convention and file-naming-convention

In particular:

| parameter | explanation |
|-----------|-------------|
| `org-name`  | A github.com organization name, e.g. `ucsd-cse-spis-2016` or `UCSB-CS56-W16` |
| `repo-pattern` | A wildcard for the repos from that organization that will be searched, e.g. `cs123-lab07-*` |
| `file-pattern` | A wildcard for the files that will be retrieved, e.g. `*.py` |
| `destination` | A directory writable by the user running the script in which to store the files.  If it doesn't already exist, it will be created. If the path or directory already exists, the new files retrieved will simply be written into this directory, either alongside the existing files, or potentially overwriting them if they have the same name. |

### Additional detail 

To use this script, each of the private repos in the organization from which you want to retrieve files should
have some naming convention associated with it.   In the limit, you could use `*` to search all repos in the organization.

Similarly, there should be a naming convention for the files you want to retrieve.  Here, `*` would retrieve only regular files (not directories) from the top level directory of each repo matches.  It is not currently possible to use this script to retrieve entire directories recursively, though that feature could be added in a future release.

## Example naming conventions

Example repo-pattern: `cs123-lab07-*`
* For individuals, this matches `cs123-lab07-Alex-T`,`cs123-lab07-Chris-L`, etc. 
* For pairs, `cs123-lab07-Alex-Chris`,`cs123-lab07-Jordan-Kelly`, etc. 
* For teams, `cs123-lab07-team01`,`cs123-lab07-team02`, etc.

Example filename-patterns:

* `data.json` matches a file called exactly `data.json` in the root of the repo
* `images/me.jpg` matches a file called `me.jpg` under the images directory in the root of the repo
* `*/*.py` matches all Python files that are exactly one directory level below the root of the repo




