# github-org-collector

A set of scripts, based on PyGithub, to collect files with particular
naming conventions from a github org

# External dependencies

You need to be able to install the Python add-on library pygithub with `pip`.

For example:
```
pip install pygithub
pip install pycurl
pip install requests
```

In particular, this script depends on `pygithub` and `pycurl`, both of which 
may need to be installed with `pip`, since they are typically not pre-installed
in most Python installations.

If the following commands fail, see [INSTALLING_PIP.md](INSTALLING_PIP.md) for hints.

If you are working on a Unix system where don't have sudo privileges, you might have success with this command; it only installs pygithub for the current user (by placing files in a hidden directory in the user's `$HOME` directory:

```
pip install --user pygithub
pip install --user pycurl
pip install --user requests
```

# The .pdf collector example

## Example Use Case: 

I  want to get all of the files ending in .pdf out of the top level directory of a bunch of repos in an organization.  My organization name is `XYZ-project-2016` and all of those repos start with `project-`, e.g. `project-Alex-Chris`, `project-Taylor-Pat`, etc.

## Solution

1. Clone this repo (the one you are now looking at), and cd into it:

```
git clone https://github.com/pconrad/github-org-collector.git
```

2. Use `pip install pygithub` and `pip install pycurl` to install the dependencies of the script.
    See instructions above for details on getting that part to work.    

3. Run this command.  This should collect the files into the directory `results` (in the current directory), 
    which will be created for you if it    does not already exist.

   ```
   python collect_file_matching_re.py -b XYZ-project-2016 project- .pdf results
   ```

   If you want to specify a different location for results, you can&mdash;for example, this puts the result directory
   in your home directory:

   ```
   python collect_file_matching_re.py -b XYZ-project-2016 project- .pdf ~/results
   ```

You will be prompted for your Github username and password; this shoudl be the github username/password of a user with Admin rights in the organization, or at the very least, the ability to read the repos in the organization in question.

The password is requested by the Python library `getpass` which takes appropriate security precautions to avoid leakage of this information.  It is passed to the Github API, and then not used further.

The retrieved files will be stored in the `results` directory, which will have two levels: the first level is the repo the files came from, and the second level is the files themslves.  

If you want to flatten, you can do so with unix commands such as:

```
mkdir ~/flat_results
cp results/*/*.pdf ~/flat_results
```

Note that in this case, there could be name collisions if two or more repos had a filename in common.  You may want to compare the results of:

```
ls results/*/*.pdf
```

and 

```
ls ~/flat_results
```

to be sure the file count is the same.

# More Detaile Usage Notes

There are currently two scripts:

* Simple: when all files you are collecting have exacty the same name: collect_private.py
* Slightly more complex: when the files you are collecting may have different names, but can be matched with a Python regular expression.

# A note on regular expressions

NOTE: If you are used to using wildcards in filenames, e.g. `cp *.pdf destination`, you may find that working with these scripts in their current form, is slightly confusing.   The parameters are NOT filename wildcards, as you would use in the Unix shell, but Python regular expressions.  The equivalent of `*.pdf`, i.e. any file that ends in `.pdf`, can be expressed simply as `.pdf`, because the regular expression will look for any substring match.

If you use `*.pdf`, that will throw an error, because the `*` operator in a regular expression needs to come after some character or group.   The equivalent of `*.pdf` 

## Detailed information on `collect_private.py`

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

## Detailed information on `collect_file_matching_re.py`

Still TBD, but you can get a synopsis of command line args and options by running:

```
python collect_file_matching_re.py -h
```

Example:
```
$ python collect_file_matching_re.py -h
usage: collect_file_matching_re.py [-h] [-b]
                                   org_name repo_pattern file_re destination

collect files from private github repos

positional arguments:
  org_name      github organization name
  repo_pattern  naming convention for repos (Python re syntax)
  file_re       regular expression in Python syntax for matching files
  destination   where to put the files retrieved

optional arguments:
  -h, --help    show this help message and exit
  -b, --binary  treat file contents as binary instead of text
$ 
```

# Feedback? Suggestions?

* Pull requests with improvements are welcomed
* Issue/bug reports may be made through github.com
