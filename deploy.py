#!/usr/bin/env python

from fabric.api import run, env, cd, settings
from subprocess import call
from sys import exit
import hosts

def config(new_instance='*'):
    ## Run state.highstate to bring the new instance up to config status
    call(['salt', new_instance, 'state.highstate'])


def app(target, branch='master', force=False):
    env.user = 'root'
    env.forward_agent = True

    with settings(host_string=target):
        run('curl -sS https://getcomposer.org/installer | php -- --install-dir=/bin')
        with cd('/var/www'):
            if force:
                run('git reset --hard origin/%s' % branch)
            run('git pull root@rs01.infra.opnreg.com:/home/webdev/open-dance.delta %s' % branch)
            run('composer.phar update')


def node(new_instance_num, node_type='base_aws'):
    ## The idea here is that we'll end up with a hostname like
    # aws03.infra.opnreg.com, i.e. <provider><num>.infra.opnreg.com
    # This could also be repurposed as <role><num>.<provider>.infra.opnreg.com
    node_dict = node_type.split('_')
    new_instance = "%s%s.infra.opnreg.com" % (node_dict[1], new_instance_num)

    ## Create new instance
    call(['salt-cloud', '-p', node_type, new_instance])
    ## Rewrite Hosts File
    hosts.recreate()
    ## Deploy Salt Configs
    config(new_instance)
    ## Call to fabric to deploy necessary app code onto new minion
    app(new_instance)
    ## Running a second deploy to cleanup anything left-over
    config(new_instance)

    ## Run an apache restart and anything else we need to cleanup pre-launch
    cleanup()

    ## TODO: insert LB call here


def cleanup():
    env.user = 'root'
    env.forward_agent = True
    run('service apache2 restart')


def destroy_node(del_instance_num):
    print del_instance_num
    del_instance = "aws%s" % del_instance_num
    ## Salt Cloud Call
    print del_instance
    call(['salt-cloud', '-d', del_instance])
