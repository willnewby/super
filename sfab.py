#!/usr/bin/env python

from fabric.api import run, env, local, cd


def aws(target_instance=False, branch='master'):
    env.user = 'root'
    env.forward_agent = True
    if target_instance:
        env.hosts = [target_instance]

    with cd('/var/www'):
#        run('git reset --hard origin/%s' % branch)
        run('git pull root@rs01.open-dance.net:/home/webdev/open-dance.delta %s' % branch)
        run('composer update')
