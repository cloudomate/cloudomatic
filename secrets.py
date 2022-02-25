import requests
import json
import time
import os
from config import project_name_dict, username, password,iam_endpoint

# return if valid token, else get token and write to file toke.json = {'token': <token value, 'timestamp' : <unix time epoch in integer>}

#post url to generate IAM
get_token_url="https://"+iam_endpoint+"/v3/auth/tokens"

project_name=project_name_dict["etisalat"]

# json body
get_token_post_json = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "name": username,
                    "password": password,
                    "domain": {
                        "name": "g42pocad"
                    }
                }
            }
        },
        "scope": {
            "project": {
                "name": project_name
            }
        }
    }
}


def get_token(get_token_post_json=get_token_post_json):
    token = return_if_valid_token(get_token_post_json)
    if token:
        return token
    else:
        return False

def generate_token():
    r = requests.post(get_token_url, data=json.dumps(get_token_post_json),headers={'content-type': 'application/json'})
    if r.status_code == 201:
        token=r.headers['X-Subject-Token']
        token_data = {"token":token,'timestamp':time.time(),'projectname':get_token_post_json['auth']['scope']['project']['name']}
        write_update_token(token_data)
        return token
    else:
        return False

def return_if_valid_token(get_token_post_json=get_token_post_json):
    if os.path.isfile('token.json'):
        with open('token.json') as f:
            data = json.load(f)
            for token in data["tokens"]:
                if token['projectname'] == get_token_post_json['auth']['scope']['project']['name']:
                    if time.time()-float(token['timestamp']) < 86400:
                        print("token exsists in cache returning valid token from cache")
                        return token['token']
                    else:
                        print("token expired generating a new one")
                        token=generate_token()
                        return token
            print("local cache does not have token for project id , generating a new one")
            token=generate_token()
            return token
    else:
        print("no token cache, generating a new one")
        token=generate_token()
        return token

def write_update_token(token_data):
    if os.path.isfile('token.json'):
        with open("token.json","r+") as f:
            print(token_data)
            data = json.load(f)
            if len(data["tokens"]) > 1:
                for token in data["tokens"]:
                    if token['projectname'] == get_token_post_json['auth']['scope']['project']['name']:
                       token['token'] = token_data['token']
                       token['timestamp'] = time.time()
                       exit
            elif data["tokens"][0]['projectname'] == get_token_post_json['auth']['scope']['project']['name']:
                data["tokens"][0]['token'] = token_data['token']
                data["tokens"][0]['timestamp'] = time.time()
                exit               
            else:
               data["tokens"].append(token_data)
            f.seek(0)
            json.dump(data,f)
    else:
        json_data={"tokens":[token_data]}
        with open("token.json","w") as f:
            json.dump(json_data,f)