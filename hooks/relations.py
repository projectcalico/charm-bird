# -*- coding: utf-8 -*-
'''
Relations for BIRD.
'''
import socket

import netaddr
import netifaces

from charmhelpers.core import hookenv
from charmhelpers.core.services.helpers import RelationContext


def router_id():
    '''
    Determine the router ID that should be used.

    This function uses the common logic of finding the IPv4 addresses
    assigned on all interfaces and picking the numerically lowest of
    them (that is not in the 127.0.0.0/8 block).
    '''
    def get_assigned_ips():
        ifs = netifaces.interfaces()

        for interface in ifs:
            if_addrs = netifaces.ifaddresses(interface)
            ip4_data = if_addrs.get(netifaces.AF_INET, [])

            for ip4 in ip4_data:
                yield netaddr.IPAddress(ip4['addr'])

    excluded_net = netaddr.IPNetwork('127.0.0.0/8')

    for addr in sorted(get_assigned_ips()):
        if addr not in excluded_net:
            return str(addr)


def resolve_domain_name(name, ip_version=4):
    '''
    Takes a domain name and resolves it to an IP address
    of a given version.

    Currently only ever returns one address.
    '''
    results = socket.getaddrinfo(name, None)
    addresses = (netaddr.IPAddress(r[4][0]) for r in results)
    filtered = (a for a in addresses if a.version == ip_version)

    try:
        addr = filtered.next()
    except StopIteration:
        addr = ''

    return str(addr)


class BgpRRRelation(RelationContext):
    '''
    Relation context for the BGP Route Reflector interface.
    '''
    name = 'bgp-route-reflector'
    interface = 'bgp-route-reflector'
    required_keys = []

    def is_ready(self):
        return True

    def _is_ready(self, data):
        return set(data.keys()).issuperset(set(['addr']))

    def get_data(self):
        peers = []

        for rid in hookenv.relation_ids(self.name):
            for unit in hookenv.related_units(rid):
                rel = hookenv.relation_get(attribute='addr',
                                           rid=rid,
                                           unit=unit)

                if rel is not None:
                    addr = resolve_domain_name(rel)

                    if addr:
                        peers.append(addr)

        self['bgp_peers'] = peers
        self['router_id'] = router_id()

        return

    def provide_data(self):
        return {'addr': hookenv.unit_get('private-address')}
