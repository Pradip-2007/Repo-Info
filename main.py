import requests
import argparse
import os
import json
PATH = os.path.expanduser("~/github_cli_token.json")#Create a file named github_cli_token.json in home directory to store the default token . This will get updated each time passinf 
def load_config():
    if not os.path.exists(PATH):
        return {}
    with open(PATH,"r") as f:
        return json.load(f)
def save_config(config):
    with open(PATH,"w") as f:
        json.dump(config,f)
def set_default_token(token):
    config = load_config()
    config["github_cli_token"] = token
    save_config(config)
def get_token():
    return load_config().get("github_cli_token")
default_token = get_token()
def user_details(username,headers):
    details ={}
    try :
        responses  = requests.get(f"https://api.github.com/users/{username}",headers=headers)
        if responses.status_code == 404:
            print(f"User {username} not found. ")
            return None
        if responses.status_code == 403:
            print("You don't have permission to access this resource .")
            return None
        if responses.status_code == 401: 
            print("Authentication failed.")   
            return None 
        data = responses.json()
        details["Username"] = data.get("login")
        details["Name"] = data.get("name") or "Not Provided "
        details["Avatar URL"] =  data.get("avatar_url") or "Not Provided "
        details["URL to the github_handle"] = data.get("html_url") or "Not Provided "
        details["Email"] = data.get("email") or "Not provided "
        details["Biodata"] = data.get("bio") or "Not provided "
        details["Followers count"] = data.get("followers")
        details["Following count"] = data.get("following")
        return details
    except Exception as e:
        print(f"Error : {e}")
        return None
def repo_details(username , reponame,headers):
    details ={} 
    try:
        response = requests.get(f"https://api.github.com/repos/{username}/{reponame}",headers=headers)
        if response.status_code == 403:
            print("You don't have permission to access this resource .")
            return None
        if response.status_code == 401: 
            print("Authentication failed.") 
        if response.status_code == 404:
            print(f"Repo {reponame} of username {username} not found ")
            return None
        data = response.json()
        details["private/Public"] = "Private" if data.get("private") else  "Public"
        details["Forks Count"] = data.get("forks_count")
        details["Stargazers Count"] = data.get("stargazers_count")
        details["Watchers count"]  = data.get("watchers_count")
        Topics = data.get("topics",[])
        details["Topics"] = ", ".join(Topics) if Topics else "No topics "
        license_info = data.get("license")
        details["License"] = license_info["name"] if license_info else "No License . "
        return details 
    except Exception as e:
        print(f"Error :{e}")
        return None

def changing_repo_details(username,reponame,headers,choice):
    response1 = requests.get(f"https://api.github.com/repos/{username}/{reponame}",headers=headers)
    if response1.status_code !=200:
        return f"Error occured"
    prev_status = "private" if response1.json().get("private") else "public"
    if choice == prev_status:
        return f"repo {reponame} is already {prev_status}"
    else:
        if choice == "private":
            payload = {
                "private":True
            }
        else :
            payload = {
                "private" : False
            }
        response = requests.patch(f"https://api.github.com/repos/{username}/{reponame}",headers=headers,json=payload)
        if response.status_code == 200 :
            return f"{reponame} is now {choice}"
        else :
            return f"Some error occured"

def create_repo(headers,payload):
    try:
        response = requests.post("https://api.github.com/user/repos",headers=headers,json=payload)
        if response.status_code == 201:
            data = response.json()
            details = {}
            details["Repository Name"] = data.get("name")
            if data.get("description"):
                details["description"] = data.get("description")
            details["visibility"] = "Private" if data.get("private") else "public"
            details["Repository url"] = data.get("html_url")
            print(f"Repository {details['Repository Name']} is created successfully")
            return details
    except Exception as e :
        print(f"Error : {e}")
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Github CLI Tool" ,description="Extracting details from username and reponame.")
    parser.add_argument('-user',"--username" , required=True,help="Github username to get details (required Argument).If not provided the program will exit with an error .")
    parser.add_argument('-repo',"--reponame",nargs="?",help="Github repo name to get details .",default=None)
    parser.add_argument('-t','--token',nargs="?",help="Access token to access own private repositories ",default=None)
    parser.add_argument('-v','--visibility',nargs="?",help="Setting visibility of your repository ",choices=["private","public"],default=None)
    parser2 = parser.add_subparsers(dest="create",required=False)
    create_parser = parser2.add_parser("create",help="Create a new repository")
    create_parser.add_argument("-n","--newreponame",required=True,help="Name of repository to be created")
    create_parser.add_argument("-d","--description",help="Repository description")
    create_parser.add_argument("-p","--repostatus",choices=["private","public"],help="Setting visibility")
    arg =  parser.parse_args()
    if arg.visibility and not arg.reponame :
        parser.error("-repo is required when using --visibility")
    if arg.token:
        headers = {
        "Authorization":f"Bearer {arg.token}",
        'Accept' : "application/vnd.github.mercy-preview+json",
        "X-GitHub-Api-Version":"2022-11-28",
        }
        if arg.token != default_token: 
            set_default_token(arg.token)
    else :
        if default_token is not None :
            headers = {
            "Authorization":f"Bearer {default_token}",
            'Accept' : "application/vnd.github.mercy-preview+json",
            "X-GitHub-Api-Version":"2022-11-28",
            } 
        else :
            headers = None
    if arg.create :
        private = True if arg.repostatus == "private" else False
        payload = {
            "name":arg.newreponame,
            "private":private,
            "description":arg.description,
            "auto_init":False
        }
        details = create_repo(headers,payload)
    elif arg.reponame is None:
        details = user_details(arg.username,headers)
    elif arg.visibility is None:
        details = repo_details(arg.username , arg.reponame , headers)
    else :
        print(changing_repo_details(arg.username,arg.reponame,headers,arg.visibility))
        details = None
    if details :
        for key , value in details.items():
            print(f"{key} : {value} ")
            