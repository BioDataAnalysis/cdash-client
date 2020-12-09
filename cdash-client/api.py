import requests
import re

from .settings import config

def create_project(session, args):
    payload = {
        "Submit": True,
        "project": _args_to_project(args)
    }
    response = session.post(f"{config['cdash_api_url']}/project.php", json=payload)

    project_created = response.status_code == 200

    if not project_created:
        raise Exception(f"The project {args.project_name} already exists")

def get_project_id(session, project_name):
    response = session.get(f"{config['cdash_api_url']}/index.php?project={project_name}")

    if response.status_code != 200:
        raise Exception(f"Could not get the data from the project {project_name}. Maybe it doesn't exist?")

    return response.json()["projectid"]

'''
    CDash does not offer any other way to get a list of users.
'''

def users_list(session):
    response = session.get(f"{config['cdash_base_url']}/ajax/findusers.php?search=%")
    users_id = re.findall('<input name="userid" type="hidden" value="(.*)">', response.text)
    emails = re.findall('\\((.+\\@.+\\..+)\\)', response.text)

    return list(zip(users_id, emails))

def users_email_list(session):
    return [email for _, email in users_list(session)]

def users_id_list(session):
    return [userid for userid, _ in users_list(session)]

def users_exist(session, user_email):
    return user_email in users_email_list(session)

def normalize_to_user_ids(users: list, existing_users: list):
    user_ids = []
    for item in users:
        userid = item
        if not userid.isnumeric():
            # look for the user id in the list of existing users
            userid = [user[0] for user in existing_users if user[1] == userid]

            if len(userid) == 0:
                raise Exception(f"User '{item}' does not exist.")

        user_ids.append(userid)
    return user_ids

def add_project_users(session, args: list):
    existing_users = users_list(session)
    user_ids = normalize_to_user_ids(args.users, existing_users)
    project_id = get_project_id(session, args.project_name) if args.project_name else args.project_id

    for idx, userid in enumerate(user_ids):

        # If only one role has been specified, then use it for every user
        role = args.users_roles[idx] if len(args.users_roles) > 1 else args.users_roles[0]

        payload = {
            "userid": userid,
            "role": role,
            "repositoryCredential": "", # TODO: figure out what this is for
            "adduser": "add user",
            f"formuser_{userid}": ""
        }

        response = session.post(f"{config['cdash_base_url']}/manageProjectRoles.php?projectid={project_id}", data=payload)

        user_added = response.status_code == 200

        if not user_added:
            # Currently ignored by the API, as it will not return a different status code if something went wrong
            raise Exception(f"The user {userid} could not be added to the project. Maybe it's missing?")

def login(email, password):
    session = requests.Session()

    response = session.get(f"{config['cdash_base_url']}/login")

    login_token = re.findall('<meta name="csrf-token" content="(.*)" \\/>', response.text)[0]

    payload = {
        "email": email,
        "password": password,
        "_token": login_token
    }

    response = session.post(f"{config['cdash_base_url']}/login", data=payload)

    if response.status_code == 401:
        raise Exception("Could not login")

    return session

def _args_to_project(args):

    if not args.project_documentation_url:
        documentation_url = config["project"]["documentation_url"].format(args.project_name)
    else:
        documentation_url = args.project_documentation_url

    project = {
        "Name": args.project_name,
        "Description": args.project_description,
        "HomeUrl": config["project"]["home_url"].format(args.project_name),
        "CvsUrl": config["project"]["cvs_url"].format(args.project_name),
        "BugTrackerFilerUrl": "", # TODO
        "BugTrackerType": config["project"]["bug_tracker_type"],
        "BugTrackerUrl": config["project"]["bug_tracker_url"].format(args.project_name),
        "BugTrackerNewIssueUrl": config["project"]["bug_tracker_new_issue_url"].format(args.project_name),
        "IssueCreation": config["project"]["issue_creation"],
        "Public": config["project"]["public"], # TODO: allow this to be set to a per-project basis
        "DocumentationUrl": documentation_url,

        # TODO: make this configurable, but optional, in settings json
        "AutoremoveMaxBuilds": 500,
        "AutoremoveTimeframe": 60,
        "CoverageThreshold": 70,
        "EmailBrokenSubmission": 1,
        "EmailMaxChars": 255,
        "EmailMaxItems": 5,
        "NightlyTime": "01:00:00 UTC",
        "ShowCoverageCode": 1,
        "TestTimeMaxStatus": 3,
        "TestTimeStd": 4,
        "TestTimeStdThreshold": 1,
        "UploadQuota": 1,
        "WarningsFilter": "",
        "ErrorsFilter": "",
        "repositories": [
            {
                "id": 0,
                "url": config["project"]["cvs_url"].format(args.project_name),
                "branch": args.project_branch,
                "username": "",
                "password": ""
            }
        ],
        "CvsViewerType": config["project"]["cvs_viewer_type"]

    }
    return project
