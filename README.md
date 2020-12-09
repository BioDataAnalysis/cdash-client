# CDash API Client

CDash is an open source, web-based software testing server. It can be used to aggregate, analyze and display the results of software testing processes submitted from clients. CDash easily handles hundreds of projects with hundreds of thousands of results.

But setting up a plethora of projects or users in CDash can be a tedious task to do.

The CDash API Client `cdash-client` is a simple Python 2.x command line tool that can aid in this process.

# Installation

Currently no installation necessary. All functionality is bundled within a single file.

# Setup

```
    $ git clone https://github.com/BioDataAnalysis/cdash-client.git
    $ cp .cdash-client.sample.json .cdash-client.json
    $ vim .cdash-client.json
```

# Configuration

The configuration is stored inside the `settings.json` file in the root directory. However, in a clean installation, this should be copied and modified according to your specific needs from the file `settings.sample.json`.

Following we will explain how these settings are being used to access the CDash API and what values are accepted.

`cdash_base_url`: Accepts an URL pointing to your CDash installation. No trailing slash.
Example: `https://your.domain`

`cdash_api_endpoint`: Accepts a folder pointing to your CDash API endpoint. Typically it's `/api/v1`. This will be appended to the end of `cdash_base_url`.
Example: `/api/v1`

`cdash_token`: Currently unused. CDash does not fully support the use of tokens for API calls, so we have to skip it for now.

`cdash_login_email`: The email to login with CDash with. The user must be allowed to create projects.

`cdash_login_password`: The password to login with CDash with.

`project`: An object of several properties useful for the creation of a project.

`project.documentation_url`: Accepts an URL which points at your projects documentation URL. It supports string formatting with the project's name as the only parameter.
Example: `https://your.domain/documentation/{0}/index.html`

`project.home_url`: Accepts an URL to be assigned as your project's home. It accepts the project's name as a single parameter.
Example: `https://github.com/YourUsername/{0}`

`project.cvs_url`: Accepts the URI to the project's Control Versioning System, typically in the form of the ssh protocol. It accepts the project's name as the only parameter.
Example: `ssh://github@github.com/YourUsername/{0}.git`

`project.bug_tracker_type`: Currently not working in CDash 3.0.0

`project.cvs_viewer_type`: Which CVS viewer should CDash use. Currently the following are available: `cgit`, `cvstrac`, `fisheye`, `github`, `gitlab`, `gitorious`, `gitweb`, `gitweb2`, `hgweb`, `stash`, `loggerhead`, `p4web`, `phab_git`, `redmine`, `allura`, `trac`, `viewcvs`, `viewvc`, `viewvc_1_1`, `websvn`

`project.public`: It sets the visibility of the project. Allowed: `true`, `false`.

# Usage

```{python}
usage: cdash-client [-h] [--create_project]
                   [--project_name PROJECT_NAME]
                   [--project_description PROJECT_DESCRIPTION]
                   [--project_branch PROJECT_BRANCH]
                   [--project_documentation_url PROJECT_DOCUMENTATION_URL]
                   [--add_project_users] [--project_id PROJECT_ID]
                   [--users USERS [USERS ...]]
                   [--users_roles USERS_ROLES [USERS_ROLES ...]]
                   [--list_users_id] [--list_users_email]
```

The client currently supports the following operations:

## Login to CDash

This is performed with all operations that require a login, like creating projects or listing private projects.
Provide the user name (typically email address) and password to login.

You can login in two ways:
- by setting `cdash_login_email` and `cdash_login_password` in `.cdash-client.json` (default)
- by adding cli arguments `--login_email <your@email.com>` for email and `--login_password <your_password>` for password

Passing the login email and password directly as arguments will override whatever is
specified in the `.cdash-client.json`

### Example

## Create new Projects

There are some hard-coded parameters that we do not need for the moment, and will be generalized later on.

### Example

```
$ python3 -m cdash-client/cdash-client --create_project --project_name=MySpecialProject --project_branch=staging
```

This will create a project in your CDash installation

## List users

We can get a list of currently available users, and either get their email or ids.

### Example

```
$ python3 -m cdash-client/cdash-client --list_users_id
```

> 1 2 3

## Add users to a project

It is possible to add users to a project by providing a list of users, the roles to be assigned to them (or a single role which will be applied to every added user) and either the project id or the project name.

It is possible to specify emails and user ids interchangeably.

### Example

Adding a list of users to a project with the same user role for everyone.

```
$ python3 -m cdash-client/cdash-client --add_project_users --project_id=10 --users 6 2 1 5 30 --user_roles 0
```

Adding a list of users to a project given its name with a role for every user

```
$ python3 -m cdash-client/cdash-client --add_project_users --project_name=MySpecialProject --users 6 user3@email.com 1 5 user@email.com --user_roles 0 1 1 2 1
```

If a user does not exist, the operation will be aborted

```
$ python3 -m cdash-client/cdash-client --add_project_users --project_id=10 --users 50 5 user@email.com 2 1 --user_roles 0
```
> Traceback (most recent call last):
  File "/usr/lib/python3.6/runpy.py", line 193, in _run_module_as_main
    "__main__", mod_spec)
  File "/usr/lib/python3.6/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "/home/acastro/BioDataAnalysis/Source/cdash-client/cdash-client/__main__.py", line 59, in <module>
    main()
  File "/home/acastro/BioDataAnalysis/Source/cdash-client/cdash-client/__main__.py", line 45, in main
    api.add_project_users(session, args)
  File "/home/acastro/BioDataAnalysis/Source/cdash-client/cdash-client/api.py", line 62, in add_project_users
    user_ids = normalize_to_user_ids(args.users, existing_users)
  File "/home/acastro/BioDataAnalysis/Source/cdash-client/cdash-client/api.py", line 55, in normalize_to_user_ids
    raise Exception(f"User '{item}' does not exist.")
Exception: User '50' does not exist.
