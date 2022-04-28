import configparser


class Constants:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.gh_issue_url = config["GITHUB_URL"]["gh_issues_url"]
        self.gh_issue_comment_url = config["GITHUB_URL"]["gh_issue_comments_url"]
        self.gh_token = config["GITHUB_URL"]["gh_token"]
        self.tm_task_url = config["TEAMWORK_URL"]["tm_create_task_url"]
        self.tm_task_comment_url = config["TEAMWORK_URL"]["tm_task_comment_url"]
        self.tm_token = config["TEAMWORK_URL"]["tm_token"]
        self.tm_cmp_url = config["TEAMWORK_URL"]["tm_cmp_url"]
