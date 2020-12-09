import argparse
import sys

from . import api

def main():

    parser = argparse.ArgumentParser(description="Create a new CDash project")

    # TODO : CDash API currently does not work with API tokens, so we have to
    # use regular email-password sessions.
    # parser.add_argument("--login_token", type=str, help="Token", required=True)
    parser.add_argument("--login_email", type=str, help="Login email", required=False)
    parser.add_argument("--login_password", type=str, help="Login password", required=False)

    parser.add_argument("--create_project", help="Creates a project", action="store_true")

    parser.add_argument("--project_name",                                                        type=str, help="The project name")
    parser.add_argument("--project_description",                                                 type=str, help="The project description")
    parser.add_argument("--project_branch",             required="--create_project" in sys.argv, type=str, help="The project branch")
    parser.add_argument("--project_documentation_url",                                           type=str, help="The URL of the project's documentation")

    parser.add_argument("--add_project_users", help="The project's users", action="store_true")

    parser.add_argument("--project_id", type=int, help="The project's identifier")
    parser.add_argument("--users", nargs="+", help="The list of users emails to add to the project", required="--add_project_users" in sys.argv)
    parser.add_argument("--users_roles", nargs="+", help="The list of user roles to be assigned to each user", required="--add_project_users" in sys.argv)

    # parser.add_argument("--list_users", help="Get back a list of users", action="store_true")
    parser.add_argument("--list_users_id", help="Get back a list of users id", action="store_true")
    parser.add_argument("--list_users_email", help="Get back a list of users email", action="store_true")

    args = parser.parse_args()

    if args["login_email"] and args["login_password"]:
        session = api.login(args.login_email, args.login_password)
    else:
        session = api.login()

    if not session:
        sys.exit("Error while loggin in: the credentials are wrong")

    if args.create_project:
        api.create_project(session, args)
        exit(0)

    if args.add_project_users:
        api.add_project_users(session, args)
        exit(0)

    if args.list_users_id:
        print(" ".join(api.users_id_list(session)))
        exit(0)

    if args.list_users_email:
        print(" ".join(api.users_email_list(session)))
        exit(0)

    exit(0)

if __name__ == '__main__':
    main()
