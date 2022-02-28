# coding=utf-8
import requests
import json
from config import subnetid,project_id_dict, elb_endpoint
import argparse
from secrets import get_token
import random
import string
import time

pos_codes = [200,201,202]

loadbalancer_id=""

project_id=project_id_dict["etisalat"]

create_elb_url = "https://"+elb_endpoint+"/v2.0/lbaas/loadbalancers"

delete_elb_url = "https://"+elb_endpoint+"/v2.0/lbaas/loadbalancers/"+loadbalancer_id

#put
update_elb_url = "https://"+elb_endpoint+"/v2.0/lbaas/loadbalancers/"+loadbalancer_id

query_elb_list_url="https://"+elb_endpoint+"/v2.0/lbaas/loadbalancers"

query_elb_url="https://"+elb_endpoint+"/v2.0/lbaas/loadbalancers/"

query_elb_tree_url="https://"+elb_endpoint+"/v2.0/lbaas/loadbalancers/"+loadbalancer_id+"/statuses"