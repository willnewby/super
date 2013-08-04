#!/usr/bin/env python


from subprocess import call
from sys import exit
import hosts
import s_fabric


def config(new_instance='*'):
    ## Run state.highstate to bring the new instance up to config status
    call(['salt', new_instance, 'state.highstate'])


def app(target_instance=False):
    sfab.aws(target_instance)


def node(new_instance_num):
    new_instance = "aws%s" % new_instance_num
    print new_instance

    ## Create new instance
    call(['salt-cloud', '-p', 'base_aws', new_instance])
    ## Rewrite Hosts File
    hosts.file_write()
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
