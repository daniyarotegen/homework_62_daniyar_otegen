def user_in_project(user, project):
    return user in project.users.all()


def user_in_issue_project(user, issue):
    return user_in_project(user, issue.project)
