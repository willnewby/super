#!/usr/bin/env python

from subprocess import call
from sys import exit
import hosts
import sfab


def config(new_instance='*'):
    ## Run state.highstate to bring the new instance up to config status
    call(['salt', new_instance, 'state.highstate'])


def app(target_instance=False):
     sfab.deploy(target_instance)


def node(new_instance_num, node_type='base_aws'):
    node_dict = node_type.split('_')
    new_instance = "%s%s.infra.opnreg.com" % (node_dict[1], new_instance_num)

    ## Create new instance
    call(['salt-cloud', '-p', node_type, new_instance])
    ## Rewrite Hosts File
    hosts.file_print()
    hosts.local_print()
    ## Deploy Salt Configs
    config(new_instance)
    ## Call to fabric to deploy necessary app code onto new minion
    app(new_instance)
    ## Possibly call to AWS/LB to place server behind the loadbalancer(s)?


def destroy_node(del_instance_num):
    print del_instance_num
    del_instance = "aws%s" % del_instance_num
    ## Salt Cloud Call
    print del_instance
    call(['salt-cloud', '-d', del_instance])
