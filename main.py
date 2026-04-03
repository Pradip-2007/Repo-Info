import requests
import argparse

def user_details(username):
    details ={}
    responses  = requests.get(f"https://api.github.com/users/{username}")
    if responses.status_code == 404:
        print(f"User {username} not found. ")
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

def repo_details(username , reponame):
    details ={}
    response2 = requests.get(f"https://api.github.com/users/{username}")
    if response2.status_code == 404:
        print(f"user {username} not found ")
        return None
    response = requests.get(f"https://api.github.com/repos/{username}/{reponame}")
    if response.status_code == 404:
        print(f"Repo {reponame} of username {username} not found ")
        return None
    data = response.json()
    details["private/Public"] = "Private" if data.get("private") else  "Public "
    details["Forks Count"] = data.get("forks_count")
    details["Stargazers Count"] = data.get("stargazers_count")
    details["Watchers count"]  = data.get("watchers_count")
    Topics = data.get("topics")
    details["Topics"] = ", ".join(Topics) if Topics else "No topics "
    license_info = data.get("license")
    details["License"] = license_info["name"] if license_info else "No License . "
    return details 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Github CLI Tool" ,description="Extracting details from username and reponame.")
    parser.add_argument('-user',"--username" , required=True,help="Github username to get details (required Argument).If not provided the program will exit with an error .")
    parser.add_argument('-repo',"--reponame",nargs="?",help="Github repo name to get details .",default=None)
    arg =  parser.parse_args()
    if arg.reponame is None:
        details = user_details(arg.username)
    else :
        details = repo_details(arg.username , arg.reponame)
    if details :
        for key , value in details.items():
            print(f"{key} : {value} \n")