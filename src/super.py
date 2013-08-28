#!/usr/bin/env python

from sys import exit
from subprocess import call
from pprint import pprint
from time import sleep
#import salt.client
import argparse
import ConfigParser
import os


## Local Modules
import deploy
import hosts
import dbbkp
import cache

## Setup Config Vars
#config = ConfigParser.ConfigParser()
#config.read([os.path.expanduser('~/.super.conf'), 'super.conf', '/etc/super.conf'])

#if not config:
#    exit('No config file read in, this can be at ~/.super.conf, super.conf, or /etc/super.conf')

#print config.items('app')

## Setup Argument Vars
parser = argparse.ArgumentParser()
parser.add_argument("action",
                    help="Either a hostname, deploy, or other action")
parser.add_argument('-n', '--number', help="""
Used with action=deploy. What number do you want to accord the new machine?
""")
parser.add_argument('-t', '--type', help="""
Used with action=deploy. Type of machine you want to deploy
""")
parser.add_argument('-b', '--branch', help="""
Used with action=push. The branch you want to deploy, defaults to 'master'
""",default='master')
parser.add_argument('-e', '--env', help="""
Used with action=push. The environment you're pushing to. 
""",default='prod')
args = parser.parse_args()




if args.action == 'deploy':
    deploy.node(args.number, args.type)

elif args.action == 'destroy':
    deploy.destroy_node(args.number)

elif args.action == 'update-one':

    node_dict = args.type.split('_')
    new_instance = "%s%s.infra.opnreg.com" % (node_dict[1], args.number)

    ## Rewrite Hosts File
    hosts.recreate()
    ## Deploy Salt Configs
    deploy.config(new_instance)
    ## Sleep waiting for salt to finish
    sleep(60)
    ## Call to fabric to deploy necessary app code onto new minion
    deploy.app(new_instance)
    ## Push out banner images, this will be going away soon
    deploy.push_images(new_instance)
    ## Run Cleanup 
    deploy.cleanup(new_instance)


elif args.action == 'banners':
    deploy.pull_images('aws02.infra.opnreg.com')

elif args.action == 'hosts':
    hosts.recreate()

elif args.action == 'push':
    ## Run state.highstate to bring everyone up to config status
    #call(['salt', '*', 'state.highstate'])

    deploy.app('all', args.branch)

elif args.action == 'status':
    print cache.get_hosts('dns')

elif args.action == 'backupdb':
    dbbkp.mysql()

else:
    ## If our arguement doesn't actually match anything,
    ## then we probably want SSH. Can do.
    print 'ssh to %s.infra.opnreg.com' % args.action
    ssh_host = "%s.infra.opnreg.com" % (args.action)
    call(['ssh', ssh_host])
