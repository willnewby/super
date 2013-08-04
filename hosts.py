#!/usr/bin/env python

from boto import ec2


def file_print():
    f = open('/srv/salt/hosts/hosts.file', 'w')
    f.write(file_assemble())
    f.close()


def file_assemble():
    hosts_head = """
127.0.0.1\t\t\tlocalhost
108.166.117.174\trs01\t\trs01.infra.opnreg.com
166.78.157.47\trs02\t\trs02.infra.opnreg.com
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
    ec2conn = ec2.connect_to_region("us-west-2")
    reservations = ec2conn.get_all_instances()

    instances = [i for r in reservations for i in r.instances]

    print instances

    for i in instances:
        ## Make sure we actually have names, otherwise named freaks out.
        if i.public_dns_name:
            print "adding %s to hosts config" % i.tags['Name']
            fqdn = i.tags['Name'] + '.infra.opnreg.com'
            hosts_body += "%s\t%s\t\t%s\n" % (i.ip_address, i.tags['Name'], fqdn)

    return hosts_head + hosts_body + hosts_foot
