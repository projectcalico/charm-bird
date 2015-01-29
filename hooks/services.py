#!/usr/bin/python

from charmhelpers.core.hookenv import config
from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers

import actions
import relations


def manage():
    services = [
        {
            'service': 'bird',
            'ports': [9905, 9906],
            'provided_data': [
                relations.BgpRRRelation(),
            ],
            'required_data': [
                relations.BgpRRRelation(),
            ],
            'data_ready': [
                helpers.render_template(
                    source='bird.conf',
                    target='/etc/bird/bird.conf'),
                actions.log_start,
            ],
        },
    ]

    # If we're using IPv6, start using BIRD.
    if config('enable-ipv6'):
        services.append({
            'service': 'bird6',
            'ports': [9905, 9906],
            'provided_data': [
                relations.BgpRRRelation(),
            ],
            'required_data': [
                relations.BgpRRRelation(),
            ],
            'data_ready': [
                helpers.render_template(
                    source='bird6.conf',
                    target='/etc/bird/bird6.conf'),
                actions.log_start,
            ],
        })

    manager = ServiceManager(services)
    manager.manage()
