#!/usr/bin/env python

from fabric.api import run, env, cd, settings

def deploy(target, branch='master', force=False):
    env.user = 'root'
    env.forward_agent = True

    with settings(host_string=target):
        run('curl -sS https://getcomposer.org/installer | php -- --install-dir=/bin')
        with cd('/var/www'):
            if force:
                run('git reset --hard origin/%s' % branch)
            run('git pull root@rs01.open-dance.net:/home/webdev/open-dance.delta %s' % branch)
            run('composer.phar update')
