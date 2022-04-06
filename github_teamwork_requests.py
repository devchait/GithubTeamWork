import requests
import base64
from stores import *
from converter import *
import json
from constants import Constants

constant = Constants()


def git_repos():
    pass


def git_branch():
    pass


def git_PR():
    pass


def git_issues():
    pass


def git_issue_comments():
    pass


def git_PR_comments():
    pass


def create_get_request():
    pass


def create_post_request():
    pass


def teamwork_projects():
    pass


def teamwork_project_board():
    pass


def create_project_task_tmw():
    pass


def create_project_task_comment_tmw():
    pass


def print_key_values(item, key=None):
    if isinstance(item, list):
        for element in item:
            # print("##############################################")
            print_key_values(element)
    elif isinstance(item, dict):
        if key:
            print(key + "--->")
        for k, v in item.items():
            print_key_values(v, key=k)
    else:
        print(key + " : " + str(item))


def set_info_to_store(store_obj, json_content, store_obj_key=None):
    if isinstance(json_content, dict) and not isinstance(json_content, list):
        for varialbe in store_obj.variables:
            if json_content and varialbe in json_content.keys():
                store_obj.setValue(varialbe, json_content[varialbe])
    else:
        store_obj.setValue(store_obj.variables, json_content)
        # print(store_obj)
    if isinstance(json_content, list):
        i = 0
        for item in json_content:
            current_obj = Store.getStoreByKey(store_obj_key, i)
            set_info_to_store(current_obj, item)
            i += 1
            store_obj.setValue(store_obj_key, current_obj)


def extract_info(inner_json, issue_obj, key):
    # print(lable_json)
    # print(key)
    i = 0
    if isinstance(inner_json, list):
        for item_content in inner_json:
            i += 1
            store_obj = Store.getStoreByKey(key, i)
            if store_obj:
                if isinstance(item_content[key], list):
                    set_info_to_store(issue_obj, item_content[key], key)
                else:
                    # if isinstance(item_content[key])
                    set_info_to_store(store_obj, item_content[key])
                    issue_obj.setValue(key, store_obj)
            else:
                if key in item_content.keys():
                    issue_obj.setValue(key, item_content[key])
    else:
        extract_info([inner_json], issue_obj, key)


def extract_issue_info(issue_json):
    issue_objs = []
    if isinstance(issue_json, list):
        j = 1
        for item_contnent in issue_json:
            current_obj = Store.getStoreByKey("issue", j)
            for key in current_obj.variables:
                extract_info(item_contnent, current_obj, key)
            j += 1
            print(current_obj)
            issue_objs.append(current_obj)
            print("!!!!!!!!!!!!!!!!!!\n\n")
    return issue_objs


def git_fetch(url, payload):
    r = requests.get(url, payload)
    return r.json()


def get_tmwork_session(url, token):
    tmwork_session = requests.Session()
    tmwork_session.auth = (token, "p")
    tmwork_session.post(url)
    return tmwork_session


def get_tmwork_response(tmwork_session, url, payload=None):
    r = tmwork_session.get(url)
    return r.json()


def post_tmwork_request(tmwork_session, url, payload):
    r = tmwork_session.post(url, data=json.dumps(payload))
    return r.json()


def convert_issues_to_tmwrk_task(gh_issues, tmwork_session, url):
    i = 1
    for issue_obj in gh_issues:
        tmwrk_task_v1_cnvrt = Gh_Issues_Tmw_Taskv1(i)
        tmwrk_task = tmwrk_task_v1_cnvrt.convert(issue_obj)
        print(tmwrk_task)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n\n")
        tmwrk_task_json = tmwrk_task_v1_cnvrt.to_json()
        print(tmwrk_task_json)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        i += 1
        response = post_tmwork_request(
            tmwork_session, tmwrk_task_cr_url, tmwrk_task_json
        )
        print(response)


if __name__ == "__main__":
    git_issue_payload = {
        "User-Agent": "chaitanay",
        "Accept": "application/vnd.github.v3+json",
        "devchait": constant.gh_token,
        "state": "all",
    }
    issues_urls = constant.gh_issue_url
    print(issues_urls)
    result = git_fetch(issues_urls, git_issue_payload)
    # print_key_values(result)

    tmwork_session = get_tmwork_session(constant.tm_cmp_url, constant.tm_token)
    tmwrk_task_cr_url = constant.tm_task_url
    issue_objs = extract_issue_info(result)
    convert_issues_to_tmwrk_task(issue_objs, tmwork_session, tmwrk_task_cr_url)
