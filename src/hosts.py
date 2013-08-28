#!/usr/bin/env python

from boto import ec2
import cache

def recreate():
    print 'Rebuilding hosts files from API'
    cache.save_hosts()
    ## Rewrite ALL the Hosts Files
    file_print('inside')
    file_print('outside')
    local_print()

def file_print(locale):
    f = open('/srv/salt/hosts/hosts.%s' % locale, 'w')
    f.write(file_assemble(locale))
    f.close()

def local_print():
    f = open('/etc/hosts', 'w')
    f.write(file_assemble())
    f.close()


def file_assemble(locale='outside'):
    hosts_head = """
127.0.0.1\t\t\tlocalhost
108.166.117.174\trs01od\t\trs01.open-dance.net
166.78.157.47\trs02\t\trs02.infra.opnreg.com
166.78.191.177\trs03\t\trs03.infra.opnreg.com
10.252.71.134\taws01.pub.openreg.local
10.252.86.209\taws02.pub.openreg.local
"""
    hosts_body = ''

    hosts_foot = """

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
"""
    for k,v in cache.get_hosts().iteritems():
        ## Make sure we actually have names, otherwise named freaks out.
        if v['public_dns_name']:
            #print "adding %s to hosts config" % i.tags['Name']
            #fqdn = i.tags['Name'] + '.infra.opnreg.com'

            if locale == 'outside':
                address = v['public_ip_address']
            else:
                address = v['private_ip_address']

            hosts_body += "%s\t%s\n" % (v['public_ip_address'], v['fqdn'])

    return hosts_head + hosts_body + hosts_foot
