# coding=utf-8
import requests
import json
from config import availability_zone,vpcid,sgid,subnetid,project_id_dict, ecs_endpoint,sshkeyname, adminpass, ubuntu_imageid, windows_imageid, centos_imageid
import argparse
from secrets import get_token
import random
import string
import time

pos_codes = [200,201,202]

project_id=project_id_dict["etisalat"]

#post
create_ecs_url="https://"+ecs_endpoint+"/v1/"+project_id+"/cloudservers"

#get
query_ecs_list_url="https://"+ecs_endpoint+"/v1/"+project_id+'/cloudservers/detail'

#get
query_ecs_url="https://"+ecs_endpoint+"/v1/"+project_id+'/cloudservers/'

#post
del_ecs_url="https://"+ecs_endpoint+"/v1/"+project_id+'/cloudservers/delete'

#get task 
query_task_url="https://"+ecs_endpoint+"/v1/"+project_id+"/jobs/"

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

ecs_config = {
    "server": {
        "availability_zone":availability_zone,
        "name": "rancher-test", 
        "imageRef": ubuntu_imageid, 
        "root_volume": {
            "volumetype": "SAS"
        }, 
        "data_volumes": [ 
            {
                "volumetype": "SAS", 
                "size": 50
            }
        ], 
        "flavorRef": "s6.large.2", 
        "vpcid": vpcid, 
        "security_groups": [
            {
                "id": sgid
            }
        ], 
        "nics": [
            {
                "subnet_id": subnetid
            }
        ], 
        "key_name": sshkeyname,
        "adminPass": adminpass,
        "count": 1, 
        "server_tags": [
            {
                "key": "key1",
                "value": "value1"
            }
        ]
    }
}

del_ecs_json  = {
    "servers": [
        {
            "id": ""
        }
    ], 
    "delete_publicip": True, 
    "delete_volume": True
   }

def query_task_status(job_id):
    token = get_token()
    url=query_task_url+job_id
    if token:
        r=requests.get(url,headers={'content-type': 'application/json','X-Auth-Token':token})
        if r.status_code in pos_codes:
            if r.json()["status"] == "SUCCESS":
                return "SUCCESS"

def wait_for_task(job_id):
    while True:
        status=query_task_status(job_id)
        if status == "SUCCESS":
            print("success")
            break
        time.sleep(15)


def query_ecs_list():
    token = get_token()
    params= {"offset":1,"limit":100}
    if token:
        r=requests.get(query_ecs_list_url,params=params,headers={'content-type': 'application/json','X-Auth-Token':token})
        if r.status_code == 200:
            return r.json()
        else:
            return r.content
    else:
        print("token error")
        return "error"   

def query_ip_from_ecs(ecs_name):
    ecs_list = query_ecs_list()
    for ecs in ecs_list["servers"]:
        if ecs["name"]==ecs_name:
            vpcid=list(ecs["addresses"].keys())[0]
            addr = ecs["addresses"][vpcid][0]['addr']
            return addr
    return False

def del_ecs(ecs_name):
    ecs_list = query_ecs_list()
    id = find_ecs_id(ecs_name,ecs_list)
    if id != "error":
        token = get_token()
        del_ecs_json["servers"][0]["id"] = id
        if token:
            print("deleting",ecs_name,id)
            r=requests.post(del_ecs_url,data=json.dumps(del_ecs_json),headers={'content-type': 'application/json','X-Auth-Token':token})
    else:
        print("ecs does not exsist")

def find_ecs_id(ecs_name,ecs_list):
    for ecs in ecs_list["servers"]:
        if ecs["name"] == ecs_name:
            id = ecs["id"]
            return id
        else:
            return "error"

def create_ecs(vmname,flavour,imageid):
    ipaddr = query_ip_from_ecs(vmname)
    if ipaddr:
        print('already exsist')
        return False
    token = get_token()
    if token != "error":
        ecs_config["server"]["name"]=vmname
        ecs_config['server']['flavorRef']=flavour
        ecs_config['server']['imageRef']=imageid
        r=requests.post(create_ecs_url,data=json.dumps(ecs_config),headers={'content-type': 'application/json','X-Auth-Token':token})
        if r.status_code in pos_codes:
            return r.json()["job_id"]
        else:
            print(r.content)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-c','--create', help='Create ECS')
    parser.add_argument("--wait",action="store_true")
    parser.add_argument('-f','--flavour', help='ECS flaour', nargs='?', default="s6.large.2")
    parser.add_argument('-o','--os', help="OS")
    parser.add_argument('-d','--delete', help='Delete ECS')
    parser.add_argument('-l','--list',help="get ECS list",action='store_true')
    parser.add_argument('-a','--queryip',help="get ip addr of ECS" )
    args = parser.parse_args()

    if (args.create):
        print('creating vm with name',args.create)
        if args.os:
            if args.os == "windows":
                imageid = windows_imageid
            elif args.os == "ubuntu":
                imageid = ubuntu_imageid
            elif args.os == "centos":
                imageid = centos_imageid
            # create_ecs(name,flaour, osimage)
            if args.wait== True:
                job_id=create_ecs(args.create,args.flavour,imageid)
                wait_for_task(job_id)
            else:
                job_id=create_ecs(args.create,args.flavour,imageid)
    elif (args.delete):
        print('deleting vm with name',args.delete)
        del_ecs(args.delete)
    elif (args.queryip):
        addr=query_ip_from_ecs(args.queryip)
        print(addr)
    elif args.list:
        h = ['Name', 'OS', 'Flavour',"IPv4 Addr"]
        ecs_list=query_ecs_list()
        print('{:<60s} {:<40s} {:<20s} {:<40}'.format(*h))
        for ecs in ecs_list["servers"]:
            vpcid=list(ecs["addresses"].keys())[0]
            detail_list=[
                         ecs['name'],
                         ecs['metadata']['image_name'],
                         ecs['flavor']['name'],
                         ecs["addresses"][vpcid][0]['addr']
                          ]
            print('{:<60s} {:<40s} {:<20s} {:<40s}'.format(*detail_list))