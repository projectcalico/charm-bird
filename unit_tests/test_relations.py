#!/usr/bin/env python

import sys
import mock
import unittest
import netifaces
from pkg_resources import resource_filename

# allow importing relations from the hooks directory
sys.path.append(resource_filename(__name__, '../hooks'))
import relations


class TestRelationHelpers(unittest.TestCase):
    @mock.patch('netifaces.interfaces')
    @mock.patch('netifaces.ifaddresses')
    def test_router_id(self, ifaddresses, interfaces):
        interfaces.return_value = ['eth0', 'lo']
        ifaddresses.return_value = {
            netifaces.AF_INET: [{'addr': '127.0.0.2'},
                                {'addr': '172.18.18.18'},
                                {'addr': '10.0.0.1'}],
            netifaces.AF_INET6: [{'addr': 'ff00::0000'}]
        }

        rid = relations.router_id()
        self.assertEqual(rid, '10.0.0.1')
        self.assertEqual(ifaddresses.call_count, 2)
        ifaddresses.assert_any_call('eth0')
        ifaddresses.assert_any_call('lo')

    @mock.patch('socket.getaddrinfo')
    def test_resolve_domain_name(self, getaddrinfo):
        getaddrinfo.return_value = [
            (0, 0, 0, 0, ('172.18.18.18', None)),
            (0, 0, 0, 0, ('ff00::0000', None)),
            (0, 0, 0, 0, ('10.0.0.1', None)),
        ]
        r4 = relations.resolve_domain_name('test')
        r6 = relations.resolve_domain_name('test', ip_version=6)

        self.assertEqual(r4, '172.18.18.18')
        self.assertEqual(r6, 'ff00::')

    @mock.patch('socket.getaddrinfo')
    def test_resolve_domain_name_handles_empty(self, getaddrinfo):
        getaddrinfo.return_value = [
            (0, 0, 0, 0, ('127.0.0.1', None)),
            (0, 0, 0, 0, ('172.18.18.18', None)),
        ]
        r = relations.resolve_domain_name('test', ip_version=6)

        self.assertEqual(r, '')


class TestRelations(unittest.TestCase):
    @mock.patch('charmhelpers.core.hookenv.relation_ids')
    @mock.patch('charmhelpers.core.hookenv.unit_get')
    def test_bgp_provides(self, unit_get, relation_ids):
        unit_get.return_value = '172.18.18.18'
        relation_ids.return_value = []
        r = relations.BgpRRRelation()

        self.assertEqual(r.name, 'bgp-route-reflector')
        self.assertEqual(r.interface, 'bgp-route-reflector')
        self.assertEqual(r.required_keys, [])

        self.assertEqual(
            r.provide_data(),
            {'addr': '172.18.18.18'}
        )
        unit_get.assert_called_with('private-address')

    @mock.patch('relations.router_id')
    @mock.patch('charmhelpers.core.hookenv.relation_ids')
    def test_bgp_no_peers(self, relation_ids, router_id):
        relation_ids.return_value = []
        router_id.return_value = '127.0.0.1'
        r = relations.BgpRRRelation()

        self.assertEqual(r['router_id'], '127.0.0.1')
        self.assertEqual(r['bgp_peers'], [])

    @mock.patch('relations.router_id')
    @mock.patch('charmhelpers.core.hookenv.relation_get')
    @mock.patch('charmhelpers.core.hookenv.related_units')
    @mock.patch('charmhelpers.core.hookenv.relation_ids')
    def test_bgp_obtains_peers(self,
                               relation_ids,
                               related_units,
                               relation_get,
                               router_id):
        # One fake relation.
        relation_ids.return_value = [1]
        # Two fake units.
        related_units.return_value = [2, 3]
        # Always the same IP.
        relation_get.return_value = '172.18.18.19'
        # Always the same router ID
        router_id.return_value = '127.0.0.1'

        r = relations.BgpRRRelation()

        self.assertItemsEqual(
            r['bgp_peers'],
            ['172.18.18.19', '172.18.18.19']
        )
        self.assertEqual(r['router_id'], '127.0.0.1')
        relation_ids.assert_called_once_with('bgp-route-reflector')
        related_units.assert_called_once_with(1)
        self.assertEqual(relation_get.call_count, 2)
        relation_get.assert_any_call(attribute='addr', rid=1, unit=2)
        relation_get.assert_any_call(attribute='addr', rid=1, unit=3)
