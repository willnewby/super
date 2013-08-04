#!/usr/bin/env python

from sys import exit
from subprocess import call
from pprint import pprint
#import salt.client
import argparse

import deploy
import hosts

parser = argparse.ArgumentParser()
parser.add_argument("action",
                    help="Either a hostname, deploy, or other action")
parser.add_argument('-n', '--number', help="""
Used with action=deploy. What number do you want to accord the new machine?
""")
parser.add_argument('-t', '--type', help="""
Used with action=deploy. Type of machine you want to deploy
""")
args = parser.parse_args()


if args.action == 'deploy':
    deploy.node(args.number, args.type)

elif args.action == 'destroy':
    deploy.destroy_node(args.number)

elif args.action == 'push_aws':
    deploy.app()

elif args.action == 'update-one':
    ## Rewrite the hosts file to verify correctness
    hosts.file_print()

    ## Call to fabric to deploy necessary app code onto everyone
    deploy.app(args.number)

    ## Run state.highstate to bring everyone up to config status
    call(['salt', '*', 'state.highstate'])


elif args.action == 'update-all':
    ## Rewrite the hosts file to verify correctness
    hosts.file_print()

    ## Call to fabric to deploy necessary app code onto everyone
    deploy.app()

    ## Run state.highstate to bring everyone up to config status
    call(['salt', '*', 'state.highstate'])

elif args.action == 'hosts':
    hosts.file_print()

else:
    ## If our arguement doesn't actually match anything,
    ## then we probably want SSH. Can do.
    ssh_host = "%s.pub.openreg.local" % args.action
    call(['ssh', ssh_host])
