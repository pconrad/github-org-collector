# github-org-collector

A set of scripts, based on PyGithub, to collect files with particular
naming conventions from a github org

# External dependencies

You need to be able to install the Python add-on library pygithub with `pip`.

For example:
```
pip install pygithub
pip install pycurl
```

In particular, this script depends on `pygithub` and `pycurl`, both of which 
may need to be installed with `pip`, since they are typically not pre-installed
in most Python installations.

If the following commands fail, see [INSTALLING_PIP.md](INSTALLING_PIP.md) for hints.

If you are working on a Unix system where don't have sudo privileges, you might have success with this command; it only installs pygithub for the current user (by placing files in a hidden directory in the user's `$HOME` directory:

```
pip install --user pygithub
pip install --user pycurl
```

# Usage

## `collect_private.py`

### Usage:

```
python collect_private.py org_name repo_pattern path destination
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
| `repo-pattern` | A substring present in the repos that will be searched, e.g. `cs123-lab07-` |
| `path` | The path of the file you will retrieve from the repo, relative to the root directory of the repo, e.g. `data.py`, `presentation.pdf`, `images/me.jpg`
| `destination` | A directory writable by the user running the script in which to store the files.  If it doesn't already exist, it will be created. If the path or directory already exists, the new files retrieved will simply be written into this directory, either alongside the existing files, or potentially overwriting them if they have the same name. |

### Additional detail 

To use this script, each of the private repos in the organization from
which you want to retrieve files should have some naming convention
associated with it.  

Similarly, there should be a naming convention for the files you want
to retrieve.  You can specify the files you want via any substring that is present 
in the filename.

## Example naming conventions

Example repo-pattern: `cs123-lab07-`
* For individuals, this matches `cs123-lab07-Alex-T`,`cs123-lab07-Chris-L`, etc. 
* For pairs, `cs123-lab07-Alex-Chris`,`cs123-lab07-Jordan-Kelly`, etc. 
* For teams, `cs123-lab07-team01`,`cs123-lab07-team02`, etc.

