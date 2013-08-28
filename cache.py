#!/usr/bin/env python

from boto import ec2
from pprint import pprint
import json
import pickle

def save_hosts():
    ec2conn = ec2.connect_to_region("us-west-2")
    reservations = ec2conn.get_all_instances()

    instances = [i for r in reservations for i in r.instances]
    dict_return = {}
    for i in instances:
        pprint(i.tags['Name'])
        dict_return[i.tags['Name']] = {
            'public_ip_address' : i.ip_address,
            'public_dns_name' : i.dns_name,
            'private_dns_name' : i.private_dns_name,
            'private_ip_address' : i.private_ip_address,
            'fqdn' : i.tags['Name']
            }
    
    cache_file = open('/tmp/super_hosts.cache.pkl', 'wb')
    pickle.dump(dict_return, cache_file)


def get_hosts(formatting='full'):
    cache_file = open('/tmp/super_hosts.cache.pkl', 'rb')
    cache_data = pickle.load(cache_file)

    if formatting == 'dns':
        return_list = []
        print cache_data
        for k in cache_data:
            return_list.append(k)
        return return_list
    else:
        return cache_data
