# coding=utf-8
import requests
import json
from config import dbname,dbuser,project_id,rds_instance_id
import sys
from secrets import get_token


#post
create_db_url='https://rds.ae-ad-1.g42cloud.com/v3/'+project_id+'/instances/'+rds_instance_id+'/database'

#delete
delete_db_url='https://rds.ae-ad-1.g42cloud.com/v3/'+project_id+'/instances/'+rds_instance_id+'/database/'+dbname

#post
authorise_db_url='https://rds.ae-ad-1.g42cloud.com/v3/'+project_id+'/instances/'+rds_instance_id+'/db_privilege'

#get 
query_db_url='https://rds.ae-ad-1.g42cloud.com/v3/'+project_id+'/instances/'+rds_instance_id+'/database/detail?page=1&limit=10'


create_rds_json = {
    "name": dbname,
    "character_set": "utf8"
}


rds_authorise_json = {
    "db_name": dbname,
    "users":[
        {
            "name":dbuser,
            "readonly": False
        }
    ]
}


def del_db(db_name):
    db_list = query_db()
    resp = if_db_exists(db_list)
    if resp == 1:
        token = get_token()
        if token:
            print("deleting",db_name)
            r=requests.delete(delete_db_url,headers={'content-type': 'application/json','X-Auth-Token':token})
            print(r.status_code,r.content)
        else:
            print("token error")
    else :
        print("db does not exist")


def query_db():
    token = get_token()
    params= {"offset":1,"limit":10}
    if token:
        r=requests.get(query_db_url,params=params,headers={'content-type': 'application/json','X-Auth-Token':token})
        if r.status_code == 200:
            return r.json()
        else:
            return "error"
    else:
        return "token error"

def if_db_exists(dblist):
    for rds in dblist["databases"]:
        if rds["name"]==dbname:
            return 1
        else:
            return 0

def authorise_db():
    token = get_token()
    if token:
        r=requests.post(authorise_db_url,data=json.dumps(rds_authorise_json),headers={'content-type': 'application/json','X-Auth-Token':token})
        if r.json()["resp"] == "successful":
            print("authorization done !")
            print(r.content)


def create_db(dbname=dbname):
    db_list = query_db()
    resp = if_db_exists(db_list)
    if resp == 1:
        del_db(dbname)
    token = get_token()
    if token:
        r=requests.post(create_db_url,data=json.dumps(create_rds_json),headers={'content-type': 'application/json','X-Auth-Token':token})
        if r.json()["resp"] == "successful":
            print(r.content)
            print("created db now authorizing...",dbuser)
            authorise_db()

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("argument missing")
        exit 
    elif len(sys.argv) == 2:
        action = sys.argv[1]
        if action == "create":
            create_db()
        elif action == "delete":
            del_db(dbname)
        